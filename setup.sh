#!/bin/bash

echo "========================================"
echo "    PhishShield Project Setup"
echo "========================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed!"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "Python found! Starting setup..."
echo

# Run the Python setup script
python3 setup_project.py

echo
echo "Setup complete!"
