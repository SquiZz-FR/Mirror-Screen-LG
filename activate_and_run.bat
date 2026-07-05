@echo off
:: Mirror Screen LG - Activate and Run Script
:: Ce script active l'environnement virtuel et garde la fenêtre ouverte pour lancer des commandes manuellement.
::
:: Usage: Double-cliquez sur ce fichier pour activer l'environnement, puis lancez vos commandes.

:: Vérifier que l'environnement virtuel existe
if not exist venv (
    echo [ERREUR] L'environnement virtuel n'existe pas.
    echo Exécutez d'abord setup.bat pour configurer le projet.
    pause
    exit /b 1
)

:: Activer l'environnement virtuel
call .\venv\Scripts\activate
if errorlevel 1 (
    echo [ERREUR] Impossible d'activer l'environnement virtuel.
    echo Essayez : .\venv\Scripts\activate
    pause
    exit /b 1
)

echo ============================================
echo [SUCCESS] Environnement virtuel activé !
echo ============================================
echo.
echo Vous pouvez maintenant lancer des commandes comme :
echo   python src/main.py --test
echo   python src/main.py --tv-ip 192.168.0.32 --passphrase ABC123
echo.
echo Pour désactiver l'environnement, tapez : deactivate
echo.

:: Garder la fenêtre ouverte pour que l'utilisateur puisse taper des commandes
cmd /k
