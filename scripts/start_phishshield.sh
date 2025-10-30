#!/bin/bash
# PhishShield - URL Phishing Detection System
# Unix/Linux shell script to start PhishShield

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║    🛡️  PhishShield - URL Phishing Detection System  🛡️     ║"
echo "║                                                              ║"
echo "║    Advanced AI-powered phishing detection using Q-Learning   ║"
echo "║    Protect yourself from malicious URLs with confidence      ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "❌ Error: Python is not installed or not in PATH"
        echo "   Please install Python 3.8+ from https://python.org"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "✅ Python found: $($PYTHON_CMD --version)"

# Check if virtual environment exists
if [ -f "venv/bin/activate" ]; then
    echo "✅ Virtual environment found"
    source venv/bin/activate
else
    echo "⚠️  Warning: No virtual environment found"
    echo "   Consider creating one with: $PYTHON_CMD -m venv venv"
fi

# Check if requirements are installed
$PYTHON_CMD -c "import django" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Error: Dependencies not installed"
    echo "   Please run: pip install -r requirements/development.txt"
    exit 1
fi

# Start PhishShield
echo "🚀 Starting PhishShield..."
$PYTHON_CMD main.py
