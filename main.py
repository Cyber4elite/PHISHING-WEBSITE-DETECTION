

#!/usr/bin/env python3
"""
PhishShield - URL Phishing Detection System
Main launcher script for the Django application

This script provides an easy way to start the PhishShield application
with proper error handling, environment setup, and user guidance.
"""

import os
import sys
import subprocess
import webbrowser
import time
import argparse
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


def print_banner():
    """Print the PhishShield banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║    🛡️  PhishShield - URL Phishing Detection System  🛡️       ║
    ║                                                              ║
    ║    Advanced AI-powered phishing detection using Q-Learning   ║
    ║    Protect yourself from malicious URLs with confidence      ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 11):
        print("❌ Error: Python 3.11 or higher is required")
        print(f"   Current version: {sys.version}")
        print("   Please upgrade Python and try again.")
        return False
    
    print(f"✅ Python version {sys.version.split()[0]} is compatible")
    return True


def check_dependencies():
    """Check if required dependencies are installed"""
    # Map import names to package names for correct installation instructions
    required_packages = {
        'django': 'Django',
        'numpy': 'numpy',
        'reportlab': 'reportlab',
        'PIL': 'Pillow',
        'decouple': 'python-decouple'
    }
    
    missing_packages = []
    
    for import_name, package_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n💡 To install missing packages, run:")
        print("   pip install -r requirements/development.txt")
        return False
    
    print("✅ All required dependencies are installed")
    return True


def check_database():
    """Check if database is properly set up"""
    try:
        from django.core.management import execute_from_command_line
        from django.conf import settings
        
        # Check if database exists and is accessible
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        print("✅ Database connection successful")
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        print("💡 To fix this, run: python manage.py migrate")
        return False


def check_model_file():
    """Check if the Q-learning model file exists"""
    model_path = Path(__file__).parent / "src" / "scanner" / "model.npy"
    
    if not model_path.exists():
        print("⚠️  Warning: Q-learning model file not found")
        print(f"   Expected location: {model_path}")
        print("   The system will use rule-based fallback detection")
        return False
    
    print("✅ Q-learning model file found")
    return True


def setup_environment():
    """Set up environment variables and configuration"""
    # Set Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'phishshield.settings')
    
    # Change to src directory for Django operations
    src_dir = Path(__file__).parent / "src"
    if src_dir.exists():
        os.chdir(src_dir)
    
    # Create necessary directories
    logs_dir = Path("../logs")
    logs_dir.mkdir(exist_ok=True)
    
    staticfiles_dir = Path("../staticfiles") 
    staticfiles_dir.mkdir(exist_ok=True)
    
    print("✅ Environment setup complete")


def run_migrations():
    """Run database migrations"""
    print("🔄 Running database migrations...")
    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Database migrations completed")
        return True
    except Exception as e:
        print(f"❌ Migration error: {e}")
        return False


def collect_static_files():
    """Collect static files for production"""
    print("🔄 Collecting static files...")
    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
        print("✅ Static files collected")
        return True
    except Exception as e:
        print(f"❌ Static files collection error: {e}")
        return False


def start_development_server(host='127.0.0.1', port=8000, auto_open=True):
    """Start the Django development server"""
    print(f"🚀 Starting PhishShield development server...")
    print(f"   Server will be available at: http://{host}:{port}/")
    print("   Press Ctrl+C to stop the server")
    print()
    
    if auto_open:
        # Open browser after a short delay
        def open_browser():
            time.sleep(2)
            try:
                webbrowser.open(f'http://{host}:{port}/')
                print("🌐 Browser opened automatically")
            except Exception:
                print("   Please open your browser and go to: http://127.0.0.1:8000/")
        
        import threading
        browser_thread = threading.Thread(target=open_browser, daemon=True)
        browser_thread.start()
    
    try:
        # Use subprocess to start Django server instead of execute_from_command_line
        print(f"   Starting Django server on {host}:{port}")
        import subprocess
        import sys
        
        # Start the server using subprocess
        process = subprocess.Popen([
            sys.executable, 'manage.py', 'runserver', f'{host}:{port}'
        ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        
        print("✅ Server started successfully!")
        print(f"   Server is running at: http://{host}:{port}/")
        print("   Press Ctrl+C to stop the server")
        print()
        
        # Stream output from the server
        try:
            for line in iter(process.stdout.readline, ''):
                if line:
                    print(line.rstrip())
        except KeyboardInterrupt:
            print("\n🛑 Stopping server...")
            process.terminate()
            process.wait()
            print("✅ Server stopped successfully")
            print("   Thank you for using PhishShield!")
            
    except Exception as e:
        print(f"❌ Server error: {e}")
        print(f"   Error type: {type(e).__name__}")
        print(f"   Current working directory: {os.getcwd()}")
        print(f"   manage.py exists: {os.path.exists('manage.py')}")
        return False
    
    return True


def start_production_server():
    """Start the production server using Gunicorn"""
    print("🚀 Starting PhishShield production server...")
    
    try:
        # Check if Gunicorn is installed
        import gunicorn
        print("✅ Gunicorn found")
    except ImportError:
        print("❌ Gunicorn not found. Installing...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'gunicorn'], check=True)
    
    try:
        # Start Gunicorn server
        subprocess.run([
            'gunicorn',
            'phishshield.wsgi:application',
            '--bind', '0.0.0.0:8000',
            '--workers', '4',
            '--timeout', '120'
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Production server error: {e}")
        return False
    
    return True


def run_tests():
    """Run the test suite"""
    print("🧪 Running PhishShield test suite...")
    
    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'test'])
        print("✅ All tests passed!")
        return True
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False


def create_superuser():
    """Create a Django superuser"""
    print("👤 Creating Django superuser...")
    
    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'createsuperuser'])
        print("✅ Superuser created successfully")
        return True
    except Exception as e:
        print(f"❌ Superuser creation error: {e}")
        return False


def show_help():
    """Show help information"""
    help_text = """
    PhishShield - URL Phishing Detection System
    
    USAGE:
        python main.py [OPTIONS]
    
    OPTIONS:
        --help, -h              Show this help message
        --version, -v           Show version information
        --host HOST             Server host (default: 127.0.0.1)
        --port PORT             Server port (default: 8000)
        --no-browser            Don't open browser automatically
        --production            Start production server (Gunicorn)
        --migrate               Run database migrations only
        --test                  Run test suite only
        --collectstatic         Collect static files only
        --createsuperuser       Create Django superuser
        --check                 Check system configuration
    
    EXAMPLES:
        python main.py                          # Start development server
        python main.py --production             # Start production server
        python main.py --test                   # Run tests
        python main.py --migrate                # Run migrations
        python main.py --host 0.0.0.0 --port 8080  # Custom host/port
    
    For more information, visit: https://github.com/your-repo/phishshield
    """
    print(help_text)


def show_version():
    """Show version information"""
    version_info = """
    PhishShield - URL Phishing Detection System
    Version: 1.0.0
    Django Version: 4.2+
    Python Version: 3.11+
    
    Features:
    - AI-powered phishing detection using Q-Learning
    - Real-time URL analysis
    - Detailed PDF reports
    - Modern responsive UI
    - Comprehensive test suite
    
    Copyright (c) 2024 PhishShield Team
    """
    print(version_info)


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="PhishShield - URL Phishing Detection System",
        add_help=False
    )
    
    parser.add_argument('--help', '-h', action='store_true', help='Show help message')
    parser.add_argument('--version', '-v', action='store_true', help='Show version information')
    parser.add_argument('--host', default='127.0.0.1', help='Server host (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=8000, help='Server port (default: 8000)')
    parser.add_argument('--no-browser', action='store_true', help="Don't open browser automatically")
    parser.add_argument('--production', action='store_true', help='Start production server')
    parser.add_argument('--migrate', action='store_true', help='Run database migrations only')
    parser.add_argument('--test', action='store_true', help='Run test suite only')
    parser.add_argument('--collectstatic', action='store_true', help='Collect static files only')
    parser.add_argument('--createsuperuser', action='store_true', help='Create Django superuser')
    parser.add_argument('--check', action='store_true', help='Check system configuration')
    
    args = parser.parse_args()
    
    # Handle help and version
    if args.help:
        show_help()
        return
    
    if args.version:
        show_version()
        return
    
    # Print banner
    print_banner()
    
    # Check system requirements
    if not check_python_version():
        sys.exit(1)
    
    # Setup environment
    setup_environment()
    
    # Check dependencies
    if not check_dependencies():
        print("\n💡 To install dependencies, run:")
        print("   python scripts/install_requirements.py development")
        sys.exit(1)
    
    # Check database
    if not check_database():
        print("\n💡 To fix database issues, run:")
        print("   python main.py --migrate")
        sys.exit(1)
    
    # Check model file
    check_model_file()
    
    # Handle specific commands
    if args.check:
        print("✅ System configuration check completed")
        return
    
    if args.migrate:
        if run_migrations():
            print("✅ Migration completed successfully")
        else:
            sys.exit(1)
        return
    
    if args.test:
        if run_tests():
            print("✅ All tests passed successfully")
        else:
            sys.exit(1)
        return
    
    if args.collectstatic:
        if collect_static_files():
            print("✅ Static files collected successfully")
        else:
            sys.exit(1)
        return
    
    if args.createsuperuser:
        if create_superuser():
            print("✅ Superuser created successfully")
        else:
            sys.exit(1)
        return
    
    # Start server
    if args.production:
        if not start_production_server():
            sys.exit(1)
    else:
        if not start_development_server(args.host, args.port, not args.no_browser):
            sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("   Please check the error message and try again")
        sys.exit(1)
