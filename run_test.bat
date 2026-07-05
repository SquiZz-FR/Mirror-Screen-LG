@echo off
:: Mirror Screen LG - Test Run Script
:: Ce script lance l'application en mode test (sans connexion TV)
::
:: Usage: Double-cliquez sur ce fichier pour tester le projet.

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

echo [INFO] Environnement virtuel activé.
echo.

echo [INFO] Lancement en mode test (sans connexion TV)...
echo Appuyez sur Ctrl+C pour arrêter.
echo.

:: Lancer en mode test avec debug activé
python src/main.py --test --debug

:: Désactiver l'environnement virtuel à la fin
call .\venv\Scripts\deactivate
