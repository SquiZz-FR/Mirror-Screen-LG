@echo off
:: Mirror Screen LG - Run Script
:: Ce script lance l'application Mirror Screen LG
::
:: Usage: Double-cliquez sur ce fichier ou exécutez-le depuis l'invite de commandes.

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

:: Afficher l'aide si aucun argument n'est fourni
if "%~1"=="" (
    python src/main.py --help
    goto END
)

:: Sinon, transmettre les arguments à l'application
python src/main.py %*

:END
:: Désactiver l'environnement virtuel
call .\venv\Scripts\deactivate

@echo on
