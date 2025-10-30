# 🛡️ PhishShield - URL Phishing Detection System

A Django-based web application that uses Q-Learning AI to detect phishing URLs and generate detailed analysis reports.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2+-green.svg)](https://djangoproject.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ Features

- 🔍 **Advanced URL Analysis**: Extracts 20+ features from URL structure, domain, and content patterns
- 🤖 **AI Detection**: Q-Learning model trained on thousands of phishing and legitimate URLs
- 📊 **Detailed Reports**: Get confidence scores, extracted features, and downloadable PDF reports
- 💾 **Database Storage**: All scan reports are saved with timestamps and detailed feature data
- 🎨 **Modern UI**: Clean, professional interface with responsive design and dark/light themes
- 🛡️ **Security**: CSRF protection, input validation, and secure data handling

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd phishshield
   ```

2. **Install requirements**
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

6. **Open your browser**
   Navigate to `http://127.0.0.1:8000`

## 📖 Documentation

Comprehensive documentation is available in the `docs/` directory:

### User Documentation
- [Installation Guide](docs/installation.md) - Detailed installation instructions
- [User Manual](docs/user-manual.md) - Complete user guide
- [FAQ](docs/faq.md) - Frequently asked questions
- [Troubleshooting](docs/troubleshooting.md) - Common issues and solutions

### Developer Documentation
- [Developer Setup](docs/developer-setup.md) - Development environment setup
- [Architecture](docs/architecture.md) - System architecture overview
- [API Reference](docs/api-reference.md) - API documentation
- [Technical Specification](docs/technical-specification.md) - Complete technical specs

### Project Documentation
- [Contributing Guide](docs/contributing.md) - How to contribute
- [Changelog](docs/changelog.md) - Version history
- [Documentation Index](docs/DOCS_INDEX.md) - Complete documentation index

## 🏗️ Project Structure

```
phishshield/
├── manage.py                 # Django management script
├── main.py                   # Application launcher
├── requirements/             # Environment-specific requirements
│   ├── base.txt
│   ├── development.txt
│   ├── production.txt
│   └── testing.txt
├── phishshield/              # Django project configuration
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── scanner/                  # Main application
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── utils.py             # ML model utilities
│   ├── tests/               # Test suite
│   └── model.npy            # Q-learning model
├── templates/                # HTML templates
├── static/                   # Static files (CSS, JS)
├── docs/                     # Documentation
└── tests/                    # Integration tests
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
python manage.py test

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```bash
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Database

By default, SQLite is used. For production, configure PostgreSQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'phishshield',
        'USER': 'username',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🚀 Deployment

### Development
```bash
python main.py
```

### Production
```bash
pip install -r requirements/production.txt
python manage.py collectstatic
gunicorn phishshield.wsgi:application
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check the [docs/](docs/) directory
- **Issues**: Open an issue on GitHub
- **Discussions**: Use GitHub Discussions for questions

## 🙏 Acknowledgments

- Django community for the excellent framework
- Machine learning community for Q-Learning algorithms
- Security researchers for phishing detection techniques

---

**PhishShield** - Protecting users from phishing attacks with AI-powered detection.

*Last updated: September 2024*
