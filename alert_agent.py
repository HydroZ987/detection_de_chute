import os
import time
import uuid
from typing import Any, Dict, Optional

try:
    import requests
except Exception:  # pragma: no cover - fallback sans requests
    requests = None


class AlertAgent:
    def __init__(
        self,
        source: str,
        server_url: Optional[str] = None,
        min_interval_s: float = 5.0,
        enabled: bool = True,
    ) -> None:
        self.source = source
        self.server_url = server_url or os.getenv("ALERT_SERVER_URL", "http://127.0.0.1:8000/alert")
        self.min_interval_s = min_interval_s
        self.enabled = enabled
        self._last_sent: Dict[str, float] = {}

    def send(
        self,
        event_type: str,
        severity: str,
        message: str,
        payload: Optional[Dict[str, Any]] = None,
    ) -> bool:
        if not self.enabled or requests is None:
            print("[AlertAgent] Envoi désactivé ou requests non disponible.")
            return False

        now = time.time()
        last = self._last_sent.get(event_type, 0.0)
        if now - last < self.min_interval_s:
            print(f"[AlertAgent] Envoi ignoré (intervalle de {self.min_interval_s}s non écoulé pour {event_type}).")
            return False

        data = {
            "id": str(uuid.uuid4()),
            "source": self.source,
            "event_type": event_type,
            "severity": severity,
            "message": message,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "payload": payload or {},
        }

        try:
            response = requests.post(self.server_url, json=data, timeout=5)
            response.raise_for_status()
            print(f"[AlertAgent] Alerte envoyée avec succès à {self.server_url} (status {response.status_code})")
            self._last_sent[event_type] = now
            return True
        except Exception as e:
            print(f"[AlertAgent] Erreur lors de l'envoi de l'alerte à {self.server_url} : {e}")
            if 'response' in locals():
                print(f"[AlertAgent] Réponse HTTP : {response.text}")
            return False
