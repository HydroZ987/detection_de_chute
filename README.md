# DAÏO v1.0 - Détection de chute par squelette 2D

<div align="center">
  <p align="center">
    Système de détection de chute intelligent utilisant MediaPipe, OpenCV, le filtre de Kalman et l'IA générative.
  </p>
</div>

## 📋 Description

Ce projet implémente un système de vidéo-surveillance capable de détecter les chutes en temps réel. Il combine des techniques de vision par ordinateur classiques et de l'intelligence artificielle moderne pour une détection robuste et une analyse contextuelle.

Le pipeline de détection se décompose en trois étapes clés :
1. **Détection** des points d'intérêt du corps humain via **MediaPipe**.
2. **Suivi** de la position et de l'accélération de ces points grâce au **filtre de Kalman**.
3. **Reconnaissance** de la chute basée sur des seuils de position, vitesse et accélération.

### ✨ Nouvelles Fonctionnalités
*   **Analyse de scène par IA** : En cas de chute détectée, une séquence d'images est envoyée à **GPT-4o** pour générer une description textuelle précise de la situation et évaluer le danger.
*   **Alertes SMS** : Intégration de **Twilio** pour envoyer des alertes (nécessite une configuration).

## 🛠️ Prérequis

Assurez-vous d'avoir Python 3.x installé. Les dépendances principales sont :

*   `opencv-python`
*   `mediapipe`
*   `numpy`
*   `twilio`
*   `openai`
*   `requests`

Vous pouvez installer les dépendances avec pip :

```bash
pip install opencv-python mediapipe numpy twilio openai requests
```

## 🚀 Installation et Configuration

1.  **Cloner le dépôt** :
    ```bash
    git clone https://github.com/HydroZ987/detection_de_chute.git
    cd detection_de_chute
    ```

2.  **Configuration de l'API OpenAI** :
    Le système utilise l'API OpenAI pour analyser les chutes. Vous devez définir votre clé API dans les variables d'environnement.
    
    *   **Windows (PowerShell)** :
        ```powershell
        $env:OPENAI_API_KEY='votre-clé-api-openai'
        ```
    *   **Linux/Mac** :
        ```bash
        export OPENAI_API_KEY='votre-clé-api-openai'
        ```

3.  **Configuration Twilio (Optionnel)** :
    Pour activer les alertes SMS, ouvrez le fichier `TestFallDetection_4.py` et modifiez les lignes suivantes avec vos identifiants Twilio :

    ```python
    account_sid = "VOTRE_ACCOUNT_SID"
    auth_token = "VOTRE_AUTH_TOKEN"
    ```

## ▶️ Utilisation

Pour lancer la détection sur la vidéo d'exemple ou votre webcam :

1.  Ouvrez `TestFallDetection_4.py`.
2.  Vérifiez la source vidéo (par défaut, il peut chercher une vidéo dans `DataVideos/` ou utiliser la webcam si configuré avec `0`).
3.  Exécutez le script :

```bash
python TestFallDetection_4.py
```

Le système affichera le flux vidéo avec le squelette détecté. En cas de chute, une alerte visuelle apparaîtra, et si configuré, une analyse IA sera déclenchée.

## 📂 Structure du Projet

*   `TestFallDetection_4.py` : Point d'entrée principal. Gère la boucle vidéo, l'intégration des modules et les appels API.
*   `FallDetectionMethod.py` : Contient la logique algorithmique pour détecter une chute (seuils de position, vitesse, accélération).
*   `PoseModule.py` : Wrapper autour de MediaPipe pour l'extraction facile des points du squelette.
*   `KalmanFilter.py` : Implémentation du filtre de Kalman pour lisser les mouvements et prédire les états.
*   `GraphicDesigner.py` : Utilitaires pour l'affichage graphique sur la vidéo.
*   `DataVideos/` : Dossier contenant les vidéos de test.
*   `output/` : Dossier où sont enregistrées les vidéos des chutes détectées.

## 🔗 Références

Basé sur les travaux présentés dans cet article Medium :
*   [Détection de chute à partir des points du squelette en 2D](https://medium.com/wanabilini/détection-de-chute-à-partir-des-points-du-squelette-en-2d-6cfaa1a7fd72)




