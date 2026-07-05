#!/bin/bash
# Mirror Screen LG - Setup Script
# Ce script configure l'environnement de développement pour le projet Mirror Screen LG
#
# Usage: chmod +x setup.sh && ./setup.sh

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction pour afficher un message d'erreur
error_msg() {
    echo -e "${RED}[ERREUR]${NC} $1"
}

# Fonction pour afficher un message d'information
info_msg() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

# Fonction pour afficher un message de succès
success_msg() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# Vérifier que Python est installé
if ! command -v python &> /dev/null; then
    error_msg "Python n'est pas installé."
    echo "Veuillez installer Python 3.8+ depuis https://www.python.org/downloads/"
    exit 1
fi

# Vérifier la version de Python
PY_VERSION=$(python --version 2>&1 | awk '{print $2}')
MAJOR_VERSION=$(echo $PY_VERSION | cut -d. -f1)
MINOR_VERSION=$(echo $PY_VERSION | cut -d. -f2)

if [ "$MAJOR_VERSION" -lt 3 ] || ([ "$MAJOR_VERSION" -eq 3 ] && [ "$MINOR_VERSION" -lt 8 ]); then
    error_msg "Python $PY_VERSION détecté. Ce projet nécessite Python 3.8 ou supérieur."
    exit 1
fi

info_msg "Python $PY_VERSION détecté."

# Créer l'environnement virtuel
if [ ! -d "venv" ]; then
    info_msg "Création de l'environnement virtuel..."
    python -m venv venv
    if [ $? -ne 0 ]; then
        error_msg "Impossible de créer l'environnement virtuel."
        echo "Vérifiez que vous avez les permissions d'écriture dans ce dossier."
        exit 1
    fi
    success_msg "Environnement virtuel créé."
else
    info_msg "Environnement virtuel déjà existant."
fi

# Activer l'environnement virtuel
source venv/bin/activate
if [ $? -ne 0 ]; then
    error_msg "Impossible d'activer l'environnement virtuel."
    echo "Essayez : source venv/bin/activate"
    exit 1
fi

info_msg "Environnement virtuel activé."

# Mettre à jour pip
info_msg "Mise à jour de pip..."
python -m pip install --upgrade pip > /dev/null 2>&1

# Installer les dépendances
info_msg "Installation des dépendances..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    error_msg "Impossible d'installer les dépendances."
    echo "Vérifiez votre connexion Internet et réessayez."
    deactivate
    exit 1
fi

# Vérifier l'installation
info_msg "Vérification des dépendances..."
python -c "
from src.screen_capture.capture import ScreenCapture
from src.network.stream_server import StreamServer
from src.network.device_connector import DeviceConnector
from src.utils.config import Config
print('[SUCCESS] Toutes les dépendances sont installées correctement !')
" 2> /dev/null

if [ $? -ne 0 ]; then
    error_msg "Certaines dépendances sont manquantes ou incompatibles."
    echo "Vérifiez le fichier requirements.txt."
    deactivate
    exit 1
fi

# Désactiver l'environnement virtuel
deactivate

echo
echo "==========================================="
success_msg "Configuration terminée avec succès !"
echo "==========================================="
echo
echo "Pour utiliser le projet :"
echo "  1. Activez l'environnement virtuel : source venv/bin/activate"
echo "  2. Lancez l'application : python src/main.py --help"
echo
echo "Exemples :"
echo "  - Mode test : python src/main.py --test"
echo "  - Avec TV : python src/main.py --tv-ip 192.168.0.32 --passphrase ABC123"
echo
