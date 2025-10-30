@echo off
echo ========================================
echo    PhishShield Project Setup
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

echo Python found! Starting setup...
echo.

python setup_project.py

echo.
echo Setup complete! Press any key to exit...
pause >nul
