#!/bin/bash
# Mirror Screen LG - Run Script
# Ce script lance l'application Mirror Screen LG
#
# Usage: chmod +x run.sh && ./run.sh [arguments]

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
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

# Vérifier que l'environnement virtuel existe
if [ ! -d "venv" ]; then
    error_msg "L'environnement virtuel n'existe pas."
    echo "Exécutez d'abord ./setup.sh pour configurer le projet."
    exit 1
fi

# Activer l'environnement virtuel
source venv/bin/activate
if [ $? -ne 0 ]; then
    error_msg "Impossible d'activer l'environnement virtuel."
    echo "Essayez : source venv/bin/activate"
    exit 1
fi

info_msg "Environnement virtuel activé."
echo

# Si aucun argument n'est fourni, afficher l'aide
if [ $# -eq 0 ]; then
    python src/main.py --help
    DEACTIVATE=1
else
    # Sinon, transmettre les arguments à l'application
    python src/main.py "$@"
    DEACTIVATE=1
fi

# Désactiver l'environnement virtuel
if [ "$DEACTIVATE" = "1" ]; then
    deactivate
fi
