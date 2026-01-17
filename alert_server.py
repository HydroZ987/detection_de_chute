import os
import asyncio
from typing import Any, Dict, List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import requests

app = FastAPI(title="MESPI Alert Server")

MAX_ALERTS = 200
ALERTS: List[Dict[str, Any]] = []
WEBSOCKETS: List[WebSocket] = []


class Alert(BaseModel):
    id: str
    source: str
    event_type: str
    severity: str
    message: str
    timestamp: str
    payload: Dict[str, Any] = {}


def send_sms_if_configured(text: str) -> None:
    sid = os.getenv("TWILIO_ACCOUNT_SID")
    token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_FROM")
    to_number = os.getenv("TWILIO_TO")

    if not all([sid, token, from_number, to_number]):
        return

    url = f"https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json"
    data = {
        "From": from_number,
        "To": to_number,
        "Body": text,
    }
    try:
        requests.post(url, data=data, auth=(sid, token), timeout=10)
    except Exception:
        pass


@app.get("/")
def index() -> HTMLResponse:
    return HTMLResponse(
        """
<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>MESPI Alertes</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 24px; background: #0b0f1a; color: #e8eefc; }
    h1 { margin: 0 0 16px; }
    .alert { padding: 12px 16px; border-radius: 8px; margin: 8px 0; background: #161b2e; border: 1px solid #2a3458; }
    .high { border-left: 6px solid #ff4d4f; }
    .medium { border-left: 6px solid #faad14; }
    .low { border-left: 6px solid #52c41a; }
    .meta { opacity: 0.7; font-size: 12px; margin-top: 4px; }
  </style>
</head>
<body>
  <h1>Alertes MESPI</h1>
  <div id="alerts"></div>

  <script>
    const alerts = document.getElementById('alerts');

    function addAlert(a) {
      const div = document.createElement('div');
      div.className = `alert ${a.severity || 'low'}`;
      div.innerHTML = `
        <div><strong>${a.event_type}</strong> — ${a.message}</div>
        <div class="meta">${a.timestamp} | ${a.source}</div>
      `;
      alerts.prepend(div);
    }

    fetch('/alerts').then(r => r.json()).then(list => list.forEach(addAlert));

    const ws = new WebSocket(`ws://${location.host}/ws`);
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      addAlert(data);
    };
  </script>
</body>
</html>
"""
    )


@app.get("/alerts")
def get_alerts() -> JSONResponse:
    return JSONResponse(ALERTS)


@app.post("/alert")
async def post_alert(alert: Alert) -> Dict[str, Any]:
    ALERTS.append(alert.dict())
    if len(ALERTS) > MAX_ALERTS:
        del ALERTS[0]

    await broadcast(alert.dict())

    sms_text = f"[{alert.severity.upper()}] {alert.event_type} - {alert.message}"
    send_sms_if_configured(sms_text)

    return {"status": "ok"}


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket) -> None:
    await ws.accept()
    WEBSOCKETS.append(ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        WEBSOCKETS.remove(ws)


async def broadcast(message: Dict[str, Any]) -> None:
    if not WEBSOCKETS:
        return

    dead = []
    for ws in WEBSOCKETS:
        try:
            await ws.send_json(message)
        except Exception:
            dead.append(ws)

    for ws in dead:
        if ws in WEBSOCKETS:
            WEBSOCKETS.remove(ws)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
