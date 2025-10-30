# PhishShield Project Setup Guide

This guide will help you set up the PhishShield project on any system quickly and easily.

## 🚀 Quick Setup (Recommended)

### Windows
```bash
# Double-click setup.bat or run in Command Prompt:
setup.bat
```

### Linux/macOS
```bash
# Make executable and run:
chmod +x setup.sh
./setup.sh
```

### Manual Setup
```bash
# Run the Python setup script directly:
python setup_project.py
```

## 📋 What the Setup Script Does

The setup script automatically:

1. ✅ **Checks Python version** (requires Python 3.8+)
2. ✅ **Creates virtual environment** (`.venv` or `venv`)
3. ✅ **Upgrades pip** to latest version
4. ✅ **Installs all dependencies** from requirements files
5. ✅ **Creates necessary directories** (logs, data, staticfiles)
6. ✅ **Sets up database** with migrations
7. ✅ **Creates run scripts** for easy startup
8. ✅ **Generates .env.example** file

## 🛠️ Manual Setup (Alternative)

If you prefer to set up manually:

### 1. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Set Up Database
```bash
cd src
python manage.py migrate
python manage.py createsuperuser  # Optional
cd ..
```

### 4. Create Directories
```bash
mkdir -p logs data staticfiles src/scanner/ds
```

## 🎯 Starting the Project

After setup, start the project:

### Windows
```bash
# Option 1: Use the generated script
start_phishshield.bat

# Option 2: Use main.py
python main.py

# Option 3: Manual Django
cd src
python manage.py runserver
```

### Linux/macOS
```bash
# Option 1: Use the generated script
./start_phishshield.sh

# Option 2: Use main.py
python main.py

# Option 3: Manual Django
cd src
python manage.py runserver
```

## 🌐 Access the Application

Once running, open your browser to:
- **Main Application**: http://127.0.0.1:8000
- **Scan Page**: http://127.0.0.1:8000/scan/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## 📁 Project Structure

```
PD_URL/
├── src/                    # Django project source
│   ├── phishshield/       # Django settings
│   ├── scanner/           # Main app
│   └── manage.py          # Django management
├── requirements/           # Python dependencies
├── logs/                  # Application logs
├── data/                  # Database and data files
├── staticfiles/           # Static files
├── setup_project.py       # Main setup script
├── setup.bat             # Windows setup script
├── setup.sh              # Linux/macOS setup script
└── main.py               # Application launcher
```

## 🔧 Configuration

### Environment Variables
Copy `.env.example` to `.env` and modify:
```bash
cp .env.example .env
```

Key settings:
- `DEBUG=True` - Development mode
- `SECRET_KEY` - Django secret key
- `ALLOWED_HOSTS` - Allowed hostnames
- `DATABASE_URL` - Database connection

### Model Configuration
The project supports multiple AI models:
- **Q-Learning Model**: `src/scanner/model.npy`
- **RandomForest Models**: `src/scanner/*.joblib`
- **Rule-Based**: Built-in fallback

## 🐛 Troubleshooting

### Common Issues

**Python Version Error**
```bash
# Check Python version
python --version
# Should be 3.8 or higher
```

**Virtual Environment Issues**
```bash
# Delete and recreate
rm -rf .venv  # or venv on Windows
python -m venv .venv
```

**Permission Errors (Linux/macOS)**
```bash
# Make scripts executable
chmod +x setup.sh
chmod +x start_phishshield.sh
```

**Database Errors**
```bash
# Reset database
cd src
rm -f db.sqlite3
python manage.py migrate
```

### Getting Help

1. Check the logs in `logs/phishshield.log`
2. Ensure all requirements are installed
3. Verify Python version compatibility
4. Check file permissions

## 📦 Dependencies

The project requires:
- **Python 3.8+**
- **Django 5.2+**
- **NumPy 2.0+**
- **Scikit-learn**
- **Joblib**
- **Other packages** (see requirements.txt)

## 🔄 Updating the Project

To update dependencies:
```bash
# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate      # Windows

# Update requirements
pip install --upgrade -r requirements.txt

# Run migrations if needed
cd src
python manage.py migrate
```

## 📝 Notes

- The setup script is idempotent (safe to run multiple times)
- Virtual environment is created in `.venv` (Linux/macOS) or `venv` (Windows)
- Database is SQLite by default (no additional setup required)
- All AI models are included in the repository

---

**Happy phishing detection! 🛡️**
