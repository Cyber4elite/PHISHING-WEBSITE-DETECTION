#!/usr/bin/env python3
"""
PhishShield Project Setup Script
================================

This script automatically sets up the PhishShield project on any system by:
1. Creating a virtual environment
2. Installing all required dependencies
3. Setting up the database
4. Running initial migrations
5. Creating necessary directories

Usage:
    python setup_project.py

Requirements:
    - Python 3.8 or higher
    - pip
    - git (optional, for cloning)
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path
import venv
import json

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_status(message, color=Colors.WHITE):
    """Print a status message with color"""
    print(f"{color}{message}{Colors.END}")

def print_header(message):
    """Print a header message"""
    print(f"\n{Colors.CYAN}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{message}{Colors.END}")
    print(f"{Colors.CYAN}{'='*60}{Colors.END}\n")

def print_success(message):
    """Print a success message"""
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_error(message):
    """Print an error message"""
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def print_warning(message):
    """Print a warning message"""
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")

def print_info(message):
    """Print an info message"""
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.END}")

def check_python_version():
    """Check if Python version is compatible"""
    print_header("Checking Python Version")
    
    version = sys.version_info
    print_info(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_error("Python 3.8 or higher is required!")
        print_info("Please upgrade Python and try again.")
        return False
    
    print_success(f"Python {version.major}.{version.minor} is compatible!")
    return True

def get_venv_path():
    """Get the virtual environment path"""
    if platform.system() == "Windows":
        return Path("venv")
    else:
        return Path(".venv")

def create_virtual_environment():
    """Create a virtual environment"""
    print_header("Creating Virtual Environment")
    
    venv_path = get_venv_path()
    
    if venv_path.exists():
        print_warning("Virtual environment already exists!")
        response = input("Do you want to recreate it? (y/N): ").strip().lower()
        if response == 'y':
            print_info("Removing existing virtual environment...")
            shutil.rmtree(venv_path)
        else:
            print_info("Using existing virtual environment...")
            return str(venv_path)
    
    print_info("Creating virtual environment...")
    try:
        venv.create(venv_path, with_pip=True)
        print_success(f"Virtual environment created at: {venv_path}")
        return str(venv_path)
    except Exception as e:
        print_error(f"Failed to create virtual environment: {e}")
        return None

def get_pip_executable(venv_path):
    """Get the pip executable path for the virtual environment"""
    venv_path = Path(venv_path)
    if platform.system() == "Windows":
        return venv_path / "Scripts" / "pip.exe"
    else:
        return venv_path / "bin" / "pip"

def get_python_executable(venv_path):
    """Get the Python executable path for the virtual environment"""
    venv_path = Path(venv_path)
    if platform.system() == "Windows":
        return venv_path / "Scripts" / "python.exe"
    else:
        return venv_path / "bin" / "python"

def upgrade_pip(venv_path):
    """Upgrade pip to the latest version"""
    print_header("Upgrading pip")
    
    pip_exe = get_pip_executable(venv_path)
    
    try:
        print_info("Upgrading pip...")
        result = subprocess.run([
            str(pip_exe), "install", "--upgrade", "pip"
        ], capture_output=True, text=True, check=True)
        
        print_success("pip upgraded successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to upgrade pip: {e}")
        print_info("Continuing with current pip version...")
        return False

def install_requirements(venv_path):
    """Install project requirements"""
    print_header("Installing Requirements")
    
    pip_exe = get_pip_executable(venv_path)
    requirements_files = [
        "requirements.txt",
        "requirements/base.txt",
        "requirements/development.txt"
    ]
    
    # Check which requirements files exist
    existing_files = []
    for req_file in requirements_files:
        if Path(req_file).exists():
            existing_files.append(req_file)
    
    if not existing_files:
        print_error("No requirements.txt files found!")
        return False
    
    print_info(f"Found requirements files: {', '.join(existing_files)}")
    
    # Install from each requirements file
    for req_file in existing_files:
        print_info(f"Installing from {req_file}...")
        try:
            result = subprocess.run([
                str(pip_exe), "install", "-r", req_file
            ], capture_output=True, text=True, check=True)
            
            print_success(f"Successfully installed requirements from {req_file}")
        except subprocess.CalledProcessError as e:
            print_error(f"Failed to install from {req_file}: {e}")
            print_info("Continuing with other requirements files...")
    
    return True

def create_directories():
    """Create necessary directories"""
    print_header("Creating Directories")
    
    directories = [
        "logs",
        "data",
        "staticfiles",
        "src/scanner/ds"
    ]
    
    for directory in directories:
        dir_path = Path(directory)
        if not dir_path.exists():
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
                print_success(f"Created directory: {directory}")
            except Exception as e:
                print_error(f"Failed to create directory {directory}: {e}")
        else:
            print_info(f"Directory already exists: {directory}")

def setup_database(venv_path):
    """Set up the database"""
    print_header("Setting up Database")
    
    python_exe = get_python_executable(venv_path)
    
    try:
        # Change to src directory
        os.chdir("src")
        
        print_info("Running database migrations...")
        result = subprocess.run([
            str(python_exe), "manage.py", "migrate"
        ], capture_output=True, text=True, check=True)
        
        print_success("Database migrations completed!")
        
        # Create superuser (optional)
        response = input("Do you want to create a superuser account? (y/N): ").strip().lower()
        if response == 'y':
            print_info("Creating superuser account...")
            subprocess.run([
                str(python_exe), "manage.py", "createsuperuser"
            ], check=True)
            print_success("Superuser account created!")
        
        # Change back to project root
        os.chdir("..")
        return True
        
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to set up database: {e}")
        os.chdir("..")  # Make sure we're back in the right directory
        return False
    except Exception as e:
        print_error(f"Unexpected error during database setup: {e}")
        os.chdir("..")
        return False

def create_run_script(venv_path):
    """Create a run script for easy project startup"""
    print_header("Creating Run Script")
    
    python_exe = get_python_executable(venv_path)
    
    if platform.system() == "Windows":
        script_content = f"""@echo off
echo Starting PhishShield...
cd src
"{python_exe}" manage.py runserver 127.0.0.1:8000
pause
"""
        script_path = "start_phishshield.bat"
    else:
        script_content = f"""#!/bin/bash
echo "Starting PhishShield..."
cd src
"{python_exe}" manage.py runserver 127.0.0.1:8000
"""
        script_path = "start_phishshield.sh"
    
    try:
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        if platform.system() != "Windows":
            os.chmod(script_path, 0o755)
        
        print_success(f"Created run script: {script_path}")
        return True
    except Exception as e:
        print_error(f"Failed to create run script: {e}")
        return False

def create_env_file():
    """Create a .env file template"""
    print_header("Creating Environment File")
    
    env_content = """# PhishShield Environment Configuration
# Copy this file to .env and modify as needed

# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite by default)
DATABASE_URL=sqlite:///db.sqlite3

# Security
CSRF_COOKIE_SECURE=False
SESSION_COOKIE_SECURE=False

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/phishshield.log

# Model Settings
MODEL_PATH=src/scanner/model.npy
CACHE_PREDICTIONS=True
CACHE_TIMEOUT=3600

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
"""
    
    try:
        with open(".env.example", 'w') as f:
            f.write(env_content)
        
        print_success("Created .env.example file")
        print_info("Copy .env.example to .env and modify as needed")
        return True
    except Exception as e:
        print_error(f"Failed to create .env.example: {e}")
        return False

def print_completion_message():
    """Print completion message with next steps"""
    print_header("Setup Complete! 🎉")
    
    print_success("PhishShield project setup completed successfully!")
    print()
    
    print_info("Next steps:")
    print("1. Copy .env.example to .env and configure your settings")
    print("2. Start the development server:")
    
    if platform.system() == "Windows":
        print("   - Run: start_phishshield.bat")
        print("   - Or: python main.py")
    else:
        print("   - Run: ./start_phishshield.sh")
        print("   - Or: python main.py")
    
    print("3. Open your browser to: http://127.0.0.1:8000")
    print()
    
    print_info("Project structure:")
    print("├── src/                 # Django project source")
    print("├── requirements/        # Python dependencies")
    print("├── logs/               # Application logs")
    print("├── data/               # Database and data files")
    print("└── staticfiles/        # Static files")
    print()
    
    print_info("For more information, check the README.md file")

def main():
    """Main setup function"""
    print_header("PhishShield Project Setup")
    
    print_info("This script will set up the PhishShield project on your system.")
    print_info("Make sure you have Python 3.8+ installed.")
    
    # Check if we're in the right directory
    if not Path("src").exists() or not Path("requirements").exists():
        print_error("Please run this script from the PD_URL directory!")
        print_info("The script expects to find 'src' and 'requirements' directories.")
        return False
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Create virtual environment
    venv_path = create_virtual_environment()
    if not venv_path:
        return False
    
    # Upgrade pip
    upgrade_pip(venv_path)
    
    # Install requirements
    if not install_requirements(venv_path):
        print_warning("Some requirements failed to install. Check the output above.")
    
    # Create directories
    create_directories()
    
    # Set up database
    setup_database(venv_path)
    
    # Create run script
    create_run_script(venv_path)
    
    # Create env file
    create_env_file()
    
    # Print completion message
    print_completion_message()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n" + Colors.YELLOW + "Setup cancelled by user." + Colors.END)
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)
