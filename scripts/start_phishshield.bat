@echo off
REM PhishShield - URL Phishing Detection System
REM Windows batch file to start PhishShield

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║    🛡️  PhishShield - URL Phishing Detection System  🛡️     ║
echo ║                                                              ║
echo ║    Advanced AI-powered phishing detection using Q-Learning   ║
echo ║    Protect yourself from malicious URLs with confidence      ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python is not installed or not in PATH
    echo    Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo ✅ Virtual environment found
    call venv\Scripts\activate.bat
) else (
    echo ⚠️  Warning: No virtual environment found
    echo    Consider creating one with: python -m venv venv
)

REM Check if requirements are installed
python -c "import django" >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Dependencies not installed
    echo    Please run: pip install -r requirements/development.txt
    pause
    exit /b 1
)

REM Start PhishShield
echo 🚀 Starting PhishShield...
python main.py

pause
