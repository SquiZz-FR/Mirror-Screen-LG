@echo off
:: Mirror Screen LG - Setup Script
:: Ce script configure l'environnement de développement pour le projet Mirror Screen LG
::
:: Usage: Double-cliquez sur ce fichier ou exécutez-le depuis l'invite de commandes.

:: Vérifier que Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installé ou n'est pas dans le PATH.
    echo Veuillez installer Python 3.8+ depuis https://www.python.org/downloads/
    echo N'oubliez pas de cocher "Add Python to PATH" pendant l'installation.
    pause
    exit /b 1
)

:: Vérifier la version de Python
for /f "tokens=2 delims= " %%v in ('python --version 2^>^&1') do set "pyversion=%%v"
if "%pyversion%" LSS "3.8" (
    echo [ERREUR] Python %pyversion% détecté. Ce projet nécessite Python 3.8 ou supérieur.
    pause
    exit /b 1
)

echo [INFO] Python %pyversion% détecté.

:: Créer l'environnement virtuel
if not exist venv (
    echo [INFO] Création de l'environnement virtuel...
    python -m venv venv
    if errorlevel 1 (
        echo [ERREUR] Impossible de créer l'environnement virtuel.
        echo Vérifiez que vous avez les permissions d'écriture dans ce dossier.
        pause
        exit /b 1
    )
    echo [SUCCESS] Environnement virtuel créé.
) else (
    echo [INFO] Environnement virtuel déjà existant.
)

:: Activer l'environnement virtuel
call .\venv\Scripts\activate
if errorlevel 1 (
    echo [ERREUR] Impossible d'activer l'environnement virtuel.
    echo Essayez : .\venv\Scripts\activate
    pause
    exit /b 1
)

echo [INFO] Environnement virtuel activé.

:: Mettre à jour pip
echo [INFO] Mise à jour de pip...
python -m pip install --upgrade pip >nul 2>&1

:: Installer les dépendances
echo [INFO] Installation des dépendances...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERREUR] Impossible d'installer les dépendances.
    echo Vérifiez votre connexion Internet et réessayez.
    call .\venv\Scripts\deactivate
    pause
    exit /b 1
)

:: Vérifier l'installation
echo [INFO] Vérification des dépendances...
python -c "
from src.screen_capture.capture import ScreenCapture
from src.network.stream_server import StreamServer
from src.network.device_connector import DeviceConnector
from src.utils.config import Config
print('[SUCCESS] Toutes les dépendances sont installées correctement !')
" 2>nul

if errorlevel 1 (
    echo [ERREUR] Certaines dépendances sont manquantes ou incompatibles.
    echo Vérifiez le fichier requirements.txt.
    call .\venv\Scripts\deactivate
    pause
    exit /b 1
)

:: Désactiver l'environnement virtuel
call .\venv\Scripts\deactivate

echo.
echo ============================================
echo [SUCCESS] Configuration terminée avec succès !
echo ============================================
echo.
echo Pour utiliser le projet :
echo  1. Activez l'environnement virtuel : .\venv\Scripts\activate
  2. Lancez l'application : python src/main.py --help
echo.
echo Exemples :
echo  - Mode test : python src/main.py --test
  - Avec TV : python src/main.py --tv-ip 192.168.0.32 --passphrase ABC123
echo.
pause
