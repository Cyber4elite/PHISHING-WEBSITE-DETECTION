#!/usr/bin/env python3
"""
PhishShield Requirements Installation Script
Automatically installs the appropriate requirements based on environment
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Error: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 11):
        print("❌ Python 3.11 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    
    print(f"✅ Python version {sys.version.split()[0]} is compatible")
    return True


def install_requirements(env_type):
    """Install requirements for specified environment"""
    requirements_file = f"requirements/{env_type}.txt"
    
    if not os.path.exists(requirements_file):
        print(f"❌ Requirements file not found: {requirements_file}")
        return False
    
    command = f"pip install -r {requirements_file}"
    return run_command(command, f"Installing {env_type} requirements")


def create_virtual_environment():
    """Create virtual environment if it doesn't exist"""
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
    
    print("🔄 Creating virtual environment...")
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Virtual environment created successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False


def activate_virtual_environment():
    """Activate virtual environment"""
    if os.name == 'nt':  # Windows
        activate_script = "venv\\Scripts\\activate"
    else:  # Unix/Linux/Mac
        activate_script = "venv/bin/activate"
    
    if not os.path.exists(activate_script):
        print("❌ Virtual environment activation script not found")
        return False
    
    print(f"✅ Virtual environment activation script found: {activate_script}")
    print("   To activate manually, run:")
    if os.name == 'nt':
        print(f"   {activate_script}")
    else:
        print(f"   source {activate_script}")
    
    return True


def main():
    """Main installation function"""
    parser = argparse.ArgumentParser(description="Install PhishShield requirements")
    parser.add_argument(
        "environment",
        choices=["development", "production", "testing", "base"],
        help="Environment type to install requirements for"
    )
    parser.add_argument(
        "--create-venv",
        action="store_true",
        help="Create virtual environment before installing"
    )
    parser.add_argument(
        "--no-venv",
        action="store_true",
        help="Skip virtual environment creation and activation"
    )
    
    args = parser.parse_args()
    
    print("🛡️  PhishShield Requirements Installation")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment if requested
    if args.create_venv and not args.no_venv:
        if not create_virtual_environment():
            sys.exit(1)
        
        if not activate_virtual_environment():
            sys.exit(1)
    
    # Install requirements
    if not install_requirements(args.environment):
        sys.exit(1)
    
    print("\n🎉 Installation completed successfully!")
    print(f"   Environment: {args.environment}")
    print("   Next steps:")
    print("   1. Activate virtual environment (if created)")
    print("   2. Run: python manage.py migrate")
    print("   3. Run: python manage.py runserver")


if __name__ == "__main__":
    main()
