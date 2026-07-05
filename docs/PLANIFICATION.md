# 📋 Planification du Projet : Mirror Screen LG

> **Objectif** : Créer un logiciel Windows ou une application pour téléviseurs LG WebOS permettant de dupliquer ou d'étendre l'écran d'un ordinateur sur la télévision.

---

## 📌 Table des Matières
1. [Analyse Initiale](#-analyse-initiale)
2. [Architecture du Projet](#-architecture-du-projet)
3. [Étapes de Développement](#-étapes-de-développement)
4. [Dépendances et Prérequis](#-dépendances-et-prérequis)
5. [Environnement de Développement](#-environnement-de-développement)
6. [Commandes de Test et Déploiement](#-commandes-de-test-et-déploiement)
7. [Prochaines Étapes](#-prochaines-étapes)
8. [Ressources Externes](#-ressources-externes)

---

## 🔍 Analyse Initiale

### État du Projet Initial
- **Dépôt GitHub** : `SquiZz-FR/Mirror-Screen-LG`
- **Contenu initial** :
  - `README.md` (documentation complète)
  - `requirements.txt` (dépendances Python)
  - `.gitignore`
- **Problème** : Aucun code source n'était présent, seulement la documentation.

### Méthodes de Mirroring Possibles
| Méthode | Description | Avantages | Inconvénients | Complexité |
|---------|-------------|-----------|---------------|------------|
| **Mode Développeur + SSH (Port 9922)** | Utiliser le mode développeur de LG pour envoyer des images via SSH. | ✅ Pas besoin de matériel supplémentaire. ✅ Fonctionne sur tous les modèles WebOS. | ❌ Latence élevée. ❌ Nécessite une connexion réseau stable. | Moyenne |
| **DLNA / Miracast** | Utiliser des protocoles de streaming comme DLNA ou Miracast. | ✅ Meilleure qualité vidéo. ✅ Moins de latence. | ❌ Nécessite un adaptateur Miracast (pour certains PC). ❌ Complexité accrue. | Élevée |
| **LG Cast (Connect SDK)** | Utiliser l'API LG Cast de Connect SDK. | ✅ Solution officielle LG. ✅ Bonne intégration. | ❌ Réservé aux applications mobiles (Android/iOS). ❌ Moins adapté pour un PC Windows. | Élevée |
| **WebSockets + Application WebOS** | Créer une application WebOS qui reçoit les frames via WebSockets. | ✅ Meilleure performance. ✅ Solution modulaire. | ❌ Nécessite de développer une application WebOS. | Élevée |

**→ Méthode choisie** : **WebSockets + Application WebOS** (meilleur compromis performance/modularité).

---

## 🏗️ Architecture du Projet

### Structure des Fichiers
```
Mirror-Screen-LG/
├── docs/
│   └── PLANIFICATION.md       # Ce fichier
├── src/
│   ├── __init__.py
│   ├── main.py                 # Point d'entrée principal
│   ├── network/
│   │   ├── __init__.py
│   │   ├── stream_server.py    # Serveur WebSocket pour le streaming
│   │   └── device_connector.py # Connexion SSH à la TV LG
│   ├── screen_capture/
│   │   ├── __init__.py
│   │   └── capture.py          # Capture d'écran (PIL/OpenCV)
│   └── utils/
│       ├── __init__.py
│       └── config.py           # Gestion de la configuration
├── tests/
│   ├── __init__.py
│   ├── test_capture.py          # Tests pour la capture d'écran
│   └── test_config.py          # Tests pour la configuration
├── .gitignore
├── README.md
└── requirements.txt
```

### Diagramme de Flux
```
+-------------------+       +---------------------+       +---------------------+
|     PC (Windows)  |       |   Serveur WebSocket |       |   TV LG WebOS       |
+-------------------+       +---------------------+       +---------------------+
         |                              |                              |
         | Capture d'écran (Pillow)     |                              |
         v                              |                              |
+-------------------+               |                              |
|   Frame (JPEG)    |-------------->|                              |
+-------------------+               |                              |
         ^                              v                              |
         |                       +---------------------+       |
         |                       |   Application WebOS |       |
         |                       |   (Enact/React/JS)  |       |
         |                       +---------------------+       |
         |                              |                              |
         +<--------------------- WebSocket -------------------->|
```

---

## 📅 Étapes de Développement

### ✅ Phase 1 : Initialisation du Projet (Terminé)
- [x] Nettoyer la structure existante.
- [x] Créer une nouvelle structure de dossiers (`src/`, `tests/`, `docs/`).
- [x] Configurer `.gitignore`.
- [x] Mettre à jour `requirements.txt`.

### ✅ Phase 2 : Implémentation des Modules de Base (Terminé)
- [x] **`src/main.py`** : Point d'entrée principal avec gestion des arguments CLI.
- [x] **`src/screen_capture/capture.py`** : Capture d'écran utilisant Pillow.
- [x] **`src/network/stream_server.py`** : Serveur WebSocket pour le streaming.
- [x] **`src/network/device_connector.py`** : Connexion SSH à la TV LG.
- [x] **`src/utils/config.py`** : Gestion de la configuration.

### ✅ Phase 3 : Tests Unitaires (Terminé)
- [x] Tests pour `ScreenCapture` (`tests/test_capture.py`).
- [x] Tests pour `Config` (`tests/test_config.py`).
- [x] Tous les tests passent (13/13).

### 🔄 Phase 4 : Développement de l'Application WebOS (À faire)
- [ ] Créer une application WebOS basique (HTML/JS) pour recevoir les frames.
- [ ] Intégrer WebSocket client pour recevoir les images.
- [ ] Afficher les images en temps réel sur la TV.
- [ ] Gérer les erreurs de connexion.

### 🔄 Phase 5 : Interface Graphique (Optionnel)
- [ ] Ajouter une interface PyQt6 pour une utilisation plus conviviale.
- [ ] Fenêtre de configuration (IP TV, passphrase, FPS, etc.).
- [ ] Boutons de contrôle (Démarrer/Arrêter le mirroring).
- [ ] Aperçu de la capture d'écran.

### 🔄 Phase 6 : Optimisations (À faire)
- [ ] Réduire la latence (compression, résolution, FPS).
- [ ] Ajouter un système de mise en cache des frames.
- [ ] Gérer les reconnexions automatiques.
- [ ] Ajouter des statistiques (FPS, latence, taille des frames).

### 🔄 Phase 7 : Documentation et Déploiement
- [ ] Documenter l'installation et l'utilisation.
- [ ] Créer un script d'installation automatique.
- [ ] Générer un exécutable Windows (PyInstaller).
- [ ] Publier sur GitHub avec des releases.

---

## 📦 Dépendances et Prérequis

### Prérequis Système
| Élément | Version | Obligatoire | Description |
|---------|---------|-------------|-------------|
| **Windows 10/11** | 64 bits | ✅ Oui | Système d'exploitation.
| **Python** | 3.8+ | ✅ Oui | Langage de développement.
| **LG WebOS TV** | 4.0+ | ✅ Oui | Téléviseur avec mode développeur.
| **Réseau Local** | - | ✅ Oui | PC et TV sur le même réseau.

### Dépendances Python (`requirements.txt`)
```text
# Core dependencies
PyQt6>=6.9.0          # Interface graphique (optionnelle)
paramiko>=3.0.0       # Connexion SSH à la TV
Pillow>=10.0.0        # Capture d'écran (PIL)
websockets>=12.0      # Serveur WebSocket

# Testing
pytest>=7.4.0         # Tests unitaires

# Optional: Pour de meilleures performances (nécessite des bibliothèques système)
# opencv-python>=4.8.0 # Alternative à Pillow pour la capture
# numpy>=1.24.0        # Traitement d'images (optionnel)
```

---

## 💻 Environnement de Développement

### 1. Installation de Python
- Télécharger Python depuis [python.org](https://www.python.org/downloads/).
- **Cocher "Add Python to PATH"** pendant l'installation.
- Vérifier l'installation :
  ```powershell
  python --version
  pip --version
  ```

### 2. Création de l'Environnement Virtuel (Recommandé)
Un environnement virtuel isole les dépendances du projet du reste du système.

#### **Sur Windows (CMD/PowerShell)**
```powershell
# Se placer dans le dossier du projet
cd C:\chemin\vers\Mirror-Screen-LG

# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement
.\[venv]\Scripts\activate

# Vérifier que l'environnement est activé (vous devriez voir (venv) au début de la ligne)
```

#### **Sur Linux/macOS (Bash)**
```bash
# Se placer dans le dossier du projet
cd /chemin/vers/Mirror-Screen-LG

# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement
source venv/bin/activate

# Vérifier que l'environnement est activé
```

### 3. Installation des Dépendances
```bash
# Mettre à jour pip
python -m pip install --upgrade pip

# Installer les dépendances du projet
pip install -r requirements.txt
```

### 4. Désactivation de l'Environnement Virtuel
```bash
# Sur Windows
.\[venv]\Scripts\deactivate

# Sur Linux/macOS
deactivate
```

---

## 🚀 Commandes de Test et Déploiement

### Commandes de Base
| Commande | Description |
|----------|-------------|
| `python src/main.py --help` | Affiche l'aide des arguments CLI. |
| `python src/main.py --test` | Lance en mode test (sans connexion TV). |
| `python src/main.py --tv-ip 192.168.0.32 --passphrase ABC123` | Lance avec une TV spécifique. |
| `python src/main.py --debug` | Active le mode debug (logs détaillés). |

### Exemples de Commandes
```bash
# Lancer en mode test (pour vérifier que tout fonctionne sans TV)
python src/main.py --test --debug

# Lancer avec une TV LG (remplacer IP et passphrase)
python src/main.py --tv-ip 192.168.0.32 --passphrase ABC123 --fps 10 --quality 85

# Lancer avec un port WebSocket personnalisé
python src/main.py --tv-ip 192.168.0.32 --passphrase ABC123 --websocket-port 8081
```

### Exécution des Tests
```bash
# Lancer tous les tests
python -m pytest tests/ -v

# Lancer un test spécifique
python -m pytest tests/test_capture.py -v

# Lancer avec couverture de code (nécessite pytest-cov)
pip install pytest-cov
python -m pytest tests/ --cov=src --cov-report=html
```

---

## 📜 Scripts de Configuration Automatique

### 1. Script Windows (`setup.bat`)
Créez un fichier **`setup.bat`** à la racine du projet :

```batch
@echo off
:: Mirror Screen LG - Setup Script
:: Ce script configure l'environnement de développement

:: Vérifier que Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installé ou n'est pas dans le PATH.
    echo Veuillez installer Python depuis https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Créer l'environnement virtuel
if not exist venv (
    echo [INFO] Création de l'environnement virtuel...
    python -m venv venv
    if errorlevel 1 (
        echo [ERREUR] Impossible de créer l'environnement virtuel.
        pause
        exit /b 1
    )
)

:: Activer l'environnement virtuel
call .\venv\Scripts\activate

:: Mettre à jour pip
python -m pip install --upgrade pip

:: Installer les dépendances
pip install -r requirements.txt

:: Vérifier l'installation
echo [INFO] Vérification des dépendances...
python -c "from src.screen_capture.capture import ScreenCapture; from src.network.stream_server import StreamServer; print('[SUCCESS] Toutes les dépendances sont installées !')"

:: Désactiver l'environnement virtuel
call .\venv\Scripts\deactivate

echo [INFO] Configuration terminée avec succès !
echo Pour activer l'environnement virtuel, exécutez : .\venv\Scripts\activate
pause
```

### 2. Script Linux/macOS (`setup.sh`)
Créez un fichier **`setup.sh`** à la racine du projet :

```bash
#!/bin/bash
# Mirror Screen LG - Setup Script
# Ce script configure l'environnement de développement

# Vérifier que Python est installé
if ! command -v python &> /dev/null; then
    echo "[ERREUR] Python n'est pas installé."
    echo "Veuillez installer Python depuis https://www.python.org/downloads/"
    exit 1
fi

# Créer l'environnement virtuel
if [ ! -d "venv" ]; then
    echo "[INFO] Création de l'environnement virtuel..."
    python -m venv venv
    if [ $? -ne 0 ]; then
        echo "[ERREUR] Impossible de créer l'environnement virtuel."
        exit 1
    fi
fi

# Activer l'environnement virtuel
source venv/bin/activate

# Mettre à jour pip
python -m pip install --upgrade pip

# Installer les dépendances
pip install -r requirements.txt

# Vérifier l'installation
echo "[INFO] Vérification des dépendances..."
python -c "from src.screen_capture.capture import ScreenCapture; from src.network.stream_server import StreamServer; print('[SUCCESS] Toutes les dépendances sont installées !')"

# Désactiver l'environnement virtuel
deactivate

echo "[INFO] Configuration terminée avec succès !"
echo "Pour activer l'environnement virtuel, exécutez : source venv/bin/activate"
```

### 3. Script de Lancement (`run.bat`)
Créez un fichier **`run.bat`** pour lancer facilement l'application :

```batch
@echo off
:: Mirror Screen LG - Run Script

:: Activer l'environnement virtuel
call .\venv\Scripts\activate

:: Lancer l'application en mode test
python src/main.py --test

:: Désactiver l'environnement virtuel
call .\venv\Scripts\deactivate
```

---

## 🎯 Prochaines Étapes

### Priorité 1 : Développer l'Application WebOS
1. **Créer une application WebOS** en HTML/JS pour recevoir les frames.
2. **Intégrer un client WebSocket** pour se connecter au serveur Python.
3. **Afficher les images** en temps réel sur la TV.
4. **Gérer les erreurs** (déconnexion, latence, etc.).

#### Exemple de Code pour l'Application WebOS
```html
<!-- index.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Mirror Screen Receiver</title>
    <style>
        body { margin: 0; overflow: hidden; background: black; }
        img { width: 100%; height: 100%; object-fit: contain; }
    </style>
</head>
<body>
    <img id="screen" src="" alt="Screen Mirroring" />
    <script>
        const ws = new WebSocket('ws://IP_PC:8080');
        const screen = document.getElementById('screen');
        
        ws.onopen = () => {
            console.log('Connected to server');
        };
        
        ws.onmessage = (event) => {
            if (event.data instanceof Blob) {
                const url = URL.createObjectURL(event.data);
                screen.src = url;
            }
        };
        
        ws.onerror = (error) => {
            console.error('WebSocket error:', error);
        };
    </script>
</body>
</html>
```

### Priorité 2 : Ajouter une Interface Graphique (PyQt6)
1. **Créer une fenêtre principale** avec PyQt6.
2. **Ajouter des champs de configuration** (IP TV, passphrase, FPS, etc.).
3. **Ajouter des boutons** (Démarrer/Arrêter, Tester la connexion).
4. **Afficher un aperçu** de la capture d'écran.

### Priorité 3 : Optimisations
1. **Réduire la latence** en ajustant la compression et la résolution.
2. **Ajouter un système de cache** pour les frames.
3. **Gérer les reconnexions** automatiques.
4. **Ajouter des statistiques** (FPS, latence, taille des frames).

---

## 🔗 Ressources Externes

### Dépôts GitHub Utiles
| Dépôt | Description | Lien |
|-------|-------------|------|
| **webOS-TV-app-samples** | Exemples officiels LG pour le développement WebOS. | [Lien](https://github.com/webOS-TV-app-samples) |
| **pradyumna-7/webOS-Dev** | Guide complet pour développer des applications WebOS. | [Lien](https://github.com/pradyumna-7/webOS-Dev) |
| **chros73/bscpylgtv** | Bibliothèque Python pour contrôler les TV LG WebOS. | [Lien](https://github.com/chros73/bscpylgtv) |
| **webosbrew/dev-manager-desktop** | Outil pour gérer le mode développeur sur WebOS. | [Lien](https://github.com/webosbrew/dev-manager-desktop) |

### Documentation Officielle LG
- [webOS TV Developer](https://webostv.developer.lge.com/) : Documentation officielle pour les développeurs.
- [webOS TV CLI](https://webostv.developer.lge.com/develop/tools) : Outil en ligne de commande pour le développement.
- [webOS TV Samples](https://webostv.developer.lge.com/develop/samples) : Exemples de code.

### Outils Recommandés
| Outil | Description | Lien |
|-------|-------------|------|
| **webOS TV IDE** | Environnement de développement intégré pour WebOS. | [Téléchargement](https://webostv.developer.lge.com/sdk/download) |
| **Visual Studio Code** | Éditeur de code avec extension WebOS. | [Lien](https://code.visualstudio.com/) |
| **Postman** | Outil pour tester les API WebSocket. | [Lien](https://www.postman.com/) |

---

## 📝 Notes Additionnelles

### Problèmes Connus
1. **OpenCV et libxcb** : Sur certains systèmes Linux, OpenCV nécessite des bibliothèques système (`libxcb-so.1`). Si vous rencontrez des erreurs, utilisez Pillow à la place (déjà implémenté).
2. **Mode Développeur LG** : Assurez-vous que le mode développeur est activé sur la TV et que l'application "Developer Mode" est installée depuis le LG Content Store.
3. **Port 9922** : Le port SSH pour le mode développeur est **9922** par défaut. Vérifiez qu'il est accessible depuis votre PC.

### Conseils de Dépannage
- **La TV n'est pas détectée** : Vérifiez que le PC et la TV sont sur le même réseau.
- **Erreur de connexion SSH** : Vérifiez la passphrase (6 caractères, sensible à la casse).
- **Problèmes de performance** : Réduisez le FPS ou la résolution.
- **Latence élevée** : Utilisez un câble Ethernet au lieu du Wi-Fi.

---

## 🏁 Conclusion

Ce document résume la planification complète du projet **Mirror Screen LG**. Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue sur le dépôt GitHub.

**Bon développement !** 🚀
