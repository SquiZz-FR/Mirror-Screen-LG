# Mirror Screen - Application de Miroir d'Écran pour LG WebOS TV

Cette application permet de diffuser l'écran de votre PC vers une TV LG WebOS en utilisant le mode développeur.

## Prérequis

- Windows 10 ou supérieur (64 bits)
- Python 3.8 ou supérieur
- Une TV LG WebOS avec le mode développeur activé
- Une connexion réseau entre le PC et la TV

## Installation

1. **Installation de Python**
   ```powershell
   # Vérifier si Python est installé
   python --version
   
   # Si Python n'est pas installé, téléchargez-le depuis python.org
   # et installez-le en cochant "Add Python to PATH"
   ```

2. **Création de l'environnement virtuel**
   ```powershell
   # Créer un environnement virtuel
   python -m venv venv
   
   # Activer l'environnement virtuel
   .\venv\Scripts\activate
   
   # Vérifier que l'environnement est activé (vous devriez voir (venv) au début de la ligne)
   ```

3. **Installation des dépendances**
   ```powershell
   # Mettre à jour pip
   python -m pip install --upgrade pip
   
   # Installer les dépendances
   pip install -r requirements.txt
   ```

## Configuration de la TV

1. **Activation du mode développeur**
   - Installez l'application "Developer Mode" depuis le LG Content Store
   - Lancez l'application et connectez-vous avec votre compte LG
   - Cliquez sur le bouton "Dev Mode Status" pour activer le mode développeur
   - Notez la passphrase de 6 caractères affichée en bas à gauche

2. **Configuration de la connexion**
   - Assurez-vous que votre PC et votre TV sont sur le même réseau
   - Notez l'adresse IP de votre TV (par défaut : 192.168.0.32)
   - Dans l'application Developer Mode, cliquez sur le bouton "Key Server"

## Utilisation

1. **Lancement de l'application**
   ```powershell
   # Activer l'environnement virtuel si ce n'est pas déjà fait
   .\venv\Scripts\activate
   
   # Lancer l'application
   python src/main.py
   ```

2. **Configuration de la connexion**
   - Dans l'onglet "Configuration", entrez la passphrase de 6 caractères affichée sur la TV
   - Cliquez sur "Définir la passphrase"
   - Allez dans l'onglet "Appareils" pour voir si la TV est détectée

3. **Démarrage du miroir d'écran**
   - Dans l'onglet "Capture", cliquez sur "Démarrer la capture"
   - Ajustez le FPS si nécessaire
   - Votre écran devrait maintenant s'afficher sur la TV

## Dépannage

1. **La TV n'est pas détectée**
   - Vérifiez que la TV et le PC sont sur le même réseau
   - Vérifiez que le mode développeur est activé
   - Vérifiez que le bouton "Key Server" est activé
   - Vérifiez que la passphrase est correcte (majuscules/minuscules comprises)

2. **Erreur de connexion SSH**
   - Vérifiez que le port 9922 est accessible
   - Vérifiez que la passphrase est correcte
   - Redémarrez l'application Developer Mode sur la TV

3. **Problèmes de performance**
   - Réduisez le FPS dans l'onglet "Capture"
   - Vérifiez la qualité de votre connexion réseau
   - Fermez les applications inutiles sur le PC

## Structure du projet

```
Mirror_Screen/
├── src/
│   ├── main.py              # Point d'entrée de l'application
│   ├── network/             # Gestion de la connexion réseau
│   │   ├── discovery.py     # Découverte des appareils
│   │   ├── device_selector.py # Sélection des appareils
│   │   └── stream_server.py # Serveur de streaming
│   └── screen_capture/      # Capture d'écran
│       ├── capture.py       # Capture de l'écran
│       └── preview.py       # Aperçu de la capture
├── venv/                    # Environnement virtuel Python
├── requirements.txt         # Dépendances Python
└── README.md               # Documentation
```

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails. 