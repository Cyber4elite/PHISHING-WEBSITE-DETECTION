#!/usr/bin/env python3
"""
PhishShield Requirements Checker
================================

This script checks if all required packages are installed and compatible.
"""

import sys
import importlib
import pkg_resources
from pathlib import Path

def check_package(package_name, min_version=None):
    """Check if a package is installed and meets version requirements"""
    try:
        module = importlib.import_module(package_name)
        version = getattr(module, '__version__', 'unknown')
        
        if min_version:
            try:
                if pkg_resources.parse_version(version) < pkg_resources.parse_version(min_version):
                    return False, version, f"Version {version} is below minimum {min_version}"
            except:
                pass
        
        return True, version, "OK"
    except ImportError:
        return False, None, "Not installed"

def main():
    """Check all requirements"""
    print("🔍 PhishShield Requirements Checker")
    print("=" * 50)
    
    # Required packages with minimum versions
    requirements = {
        'django': '5.0',
        'numpy': '2.0',
        'scikit-learn': '1.0',
        'joblib': '1.0',
        'PIL': None,  # Pillow
        'requests': None,
    }
    
    all_good = True
    
    for package, min_version in requirements.items():
        installed, version, status = check_package(package, min_version)
        
        if installed:
            print(f"✅ {package}: {version}")
        else:
            print(f"❌ {package}: {status}")
            all_good = False
    
    print("\n" + "=" * 50)
    
    if all_good:
        print("🎉 All requirements are satisfied!")
        print("You can run the PhishShield project.")
    else:
        print("⚠️  Some requirements are missing or outdated.")
        print("Run 'python setup_project.py' to install them.")
    
    # Check Python version
    python_version = sys.version_info
    print(f"\nPython version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("❌ Python 3.8+ is required!")
        all_good = False
    else:
        print("✅ Python version is compatible")
    
    return 0 if all_good else 1

if __name__ == "__main__":
    sys.exit(main())
