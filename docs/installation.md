# PhishShield Installation Guide

This guide will help you install and set up PhishShield on your system.

## 📋 Prerequisites

Before installing PhishShield, ensure you have:

- **Python 3.8 or higher** (recommended: Python 3.9+)
- **pip** (Python package installer)
- **Git** (for cloning the repository)
- **4GB RAM minimum** (8GB recommended)
- **1GB free disk space**

### Check Python Version

```bash
python --version
# or
python3 --version
```

If Python is not installed, download it from [python.org](https://python.org).

## 🚀 Installation Methods

### Method 1: Quick Installation (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd phishshield
   ```

2. **Run the installation script**
   ```bash
   python install_requirements.py development --create-venv
   ```

3. **Activate virtual environment**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

4. **Set up the database**
   ```bash
   python manage.py migrate
   ```

5. **Start the application**
   ```bash
   python main.py
   ```

### Method 2: Manual Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd phishshield
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

4. **Install requirements**
   ```bash
   pip install -r requirements/development.txt
   ```

5. **Set up the database**
   ```bash
   python manage.py migrate
   ```

6. **Start the application**
   ```bash
   python main.py
   ```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# .env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Database Configuration

By default, PhishShield uses SQLite. For production, consider PostgreSQL:

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'phishshield',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🧪 Verify Installation

1. **Start the application**
   ```bash
   python main.py
   ```

2. **Open your browser**
   Navigate to `http://127.0.0.1:8000`

3. **Test the system**
   - Enter a test URL (e.g., `https://example.com`)
   - Click "Analyze URL"
   - Verify results are displayed

## 🐛 Troubleshooting

### Common Issues

#### Python Version Error
```
❌ Python 3.8 or higher is required
```
**Solution**: Install Python 3.8+ from [python.org](https://python.org)

#### Module Not Found Error
```
ModuleNotFoundError: No module named 'django'
```
**Solution**: Ensure virtual environment is activated and requirements are installed

#### Database Error
```
django.db.utils.OperationalError: no such table
```
**Solution**: Run `python manage.py migrate`

#### Port Already in Use
```
Error: [Errno 98] Address already in use
```
**Solution**: Use a different port: `python manage.py runserver 8001`

### Getting Help

If you encounter issues:

1. Check the [Troubleshooting Guide](troubleshooting.md)
2. Review the [FAQ](faq.md)
3. Open an issue on the project repository

## 🔄 Updating PhishShield

To update to the latest version:

1. **Pull latest changes**
   ```bash
   git pull origin main
   ```

2. **Update requirements**
   ```bash
   pip install -r requirements/development.txt --upgrade
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Restart the application**
   ```bash
   python main.py
   ```

## 🗑️ Uninstalling PhishShield

To remove PhishShield:

1. **Stop the application** (Ctrl+C)

2. **Deactivate virtual environment**
   ```bash
   deactivate
   ```

3. **Remove project directory**
   ```bash
   rm -rf phishshield
   ```

4. **Remove virtual environment** (optional)
   ```bash
   rm -rf venv
   ```

## 📚 Next Steps

After successful installation:

1. Read the [User Manual](user-manual.md) to learn how to use PhishShield
2. Check the [Configuration Guide](configuration.md) for advanced settings
3. Review the [Developer Setup](developer-setup.md) if you plan to contribute

## 🆘 Support

Need help with installation?

- Check the [Troubleshooting Guide](troubleshooting.md)
- Review the [FAQ](faq.md)
- Open an issue on the project repository

---

*Last updated: September 2024*
*Installation Guide version: 1.0.0*
