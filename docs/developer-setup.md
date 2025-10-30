# PhishShield Developer Setup Guide

## Overview

This guide is for developers who want to contribute to, modify, or extend the PhishShield application. It covers everything from initial setup to advanced development workflows.

## Prerequisites

- **Python 3.8 or higher** (recommended: Python 3.9+)
- **pip** (Python package installer)
- **Git** (for version control)
- **A code editor** (VS Code, PyCharm, etc.)
- **Basic knowledge** of Django, Python, and web development

## Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd phishshield
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies
```bash
# Install development dependencies
pip install -r requirements/development.txt

# Or use the installation script
python install_requirements.py development --create-venv
```

### 4. Set Up Database
```bash
python manage.py migrate
```

### 5. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 6. Start Development Server
```bash
python main.py
# or
python manage.py runserver
```

## Development Environment Setup

### Environment Variables

Create a `.env` file in the project root:

```bash
# .env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### IDE Configuration

#### VS Code

Create `.vscode/settings.json`:
```json
{
    "python.defaultInterpreterPath": "./venv/Scripts/python.exe",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": [
        "."
    ],
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        "**/node_modules": true,
        "**/.pytest_cache": true
    }
}
```

#### PyCharm

1. Open project in PyCharm
2. Configure Python interpreter to use virtual environment
3. Enable Django support in project settings
4. Configure test runner to use pytest

## Project Structure Deep Dive

```
phishshield/
├── manage.py                 # Django management script
├── main.py                   # Application launcher
├── requirements/             # Environment-specific requirements
│   ├── base.txt             # Core dependencies
│   ├── development.txt      # Development tools
│   ├── production.txt       # Production dependencies
│   └── testing.txt          # Testing dependencies
├── phishshield/             # Django project configuration
│   ├── settings.py          # Django settings
│   ├── urls.py             # Main URL routing
│   └── wsgi.py             # WSGI configuration
├── scanner/                 # Main application
│   ├── models.py           # Database models
│   ├── views.py            # View functions
│   ├── utils.py            # ML utilities
│   ├── admin.py            # Admin interface
│   ├── forms.py            # Form definitions
│   ├── urls.py             # App URL routing
│   ├── tests/              # Test suite
│   │   ├── test_models.py
│   │   ├── test_views.py
│   │   ├── test_forms.py
│   │   └── test_utils.py
│   └── migrations/         # Database migrations
├── templates/              # HTML templates
├── static/                 # Static files
│   ├── css/styles.css
│   ├── js/main.js
│   └── images/
├── docs/                   # Documentation
└── logs/                   # Application logs
```

## Development Workflow

### 1. Code Style and Quality

#### Black (Code Formatter)
```bash
# Format all Python files
black .

# Check formatting without making changes
black --check .
```

#### Flake8 (Linting)
```bash
# Run linting
flake8 .

# Run with specific configuration
flake8 --config=.flake8 .
```

#### Pre-commit Hooks
```bash
# Install pre-commit hooks
pre-commit install

# Run hooks on all files
pre-commit run --all-files
```

### 2. Testing

#### Running Tests
```bash
# Run all tests
python manage.py test

# Run specific test module
python manage.py test scanner.tests.test_models

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report
```

#### Test Structure
```python
# tests/test_models.py
from django.test import TestCase
from scanner.models import ScanReport

class ScanReportModelTest(TestCase):
    def setUp(self):
        self.report = ScanReport.objects.create(
            url='https://example.com',
            result='legitimate',
            confidence=0.95,
            features={}
        )
    
    def test_str_representation(self):
        self.assertEqual(str(self.report), 'Scan Report for https://example.com - legitimate')
```

### 3. Database Management

#### Creating Migrations
```bash
# Create migrations for model changes
python manage.py makemigrations

# Create migrations for specific app
python manage.py makemigrations scanner

# Create empty migration
python manage.py makemigrations --empty scanner
```

#### Applying Migrations
```bash
# Apply all migrations
python manage.py migrate

# Apply specific migration
python manage.py migrate scanner 0001

# Show migration status
python manage.py showmigrations
```

### 4. Static Files

#### Collecting Static Files
```bash
# Collect static files for production
python manage.py collectstatic

# Collect with specific settings
python manage.py collectstatic --settings=phishshield.settings.production
```

## Adding New Features

### 1. Adding a New Model
```python
# scanner/models.py
class NewModel(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
```

### 2. Adding a New View
```python
# scanner/views.py
from django.shortcuts import render
from django.http import JsonResponse

def new_view(request):
    if request.method == 'GET':
        return render(request, 'new_template.html')
    elif request.method == 'POST':
        # Handle POST data
        return JsonResponse({'status': 'success'})
```

### 3. Adding a New URL Pattern
```python
# scanner/urls.py
urlpatterns = [
    # ... existing patterns
    path('new-endpoint/', views.new_view, name='new_view'),
]
```

### 4. Adding a New Template
```html
<!-- templates/new_template.html -->
{% extends 'base.html' %}

{% block title %}New Feature{% endblock %}

{% block content %}
<h1>New Feature</h1>
<p>This is a new feature.</p>
{% endblock %}
```

## Machine Learning Integration

### Adding New Features
```python
# scanner/utils.py
def extract_new_feature(url):
    """Extract a new feature from URL"""
    # Implementation
    return feature_value

def extract_features(url):
    features = {}
    # ... existing features
    features['new_feature'] = extract_new_feature(url)
    return features
```

### Updating the Model
```python
# scanner/utils.py
def predict_phishing(url):
    features = extract_features(url)
    
    # Update feature vector
    feature_vector = np.array([
        # ... existing features
        features['new_feature']
    ]).reshape(1, -1)
    
    # Model prediction logic
    return result
```

### Testing ML Components
```python
# tests/test_utils.py
from scanner.utils import extract_features, predict_phishing

class MLUtilsTest(TestCase):
    def test_extract_features(self):
        url = 'https://example.com'
        features = extract_features(url)
        self.assertIn('new_feature', features)
    
    def test_predict_phishing(self):
        url = 'https://example.com'
        result = predict_phishing(url)
        self.assertIn('prediction', result)
        self.assertIn('confidence', result)
```

## API Development

### Adding New API Endpoints
```python
# scanner/api_views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
def api_scan_history(request):
    """Get scan history"""
    reports = ScanReport.objects.all()[:10]
    data = [{'url': r.url, 'result': r.result} for r in reports]
    return Response(data)
```

### API URL Configuration
```python
# scanner/api_urls.py
from django.urls import path
from . import api_views

urlpatterns = [
    path('scan-history/', api_views.api_scan_history, name='api_scan_history'),
]
```

## Performance Optimization

### Database Optimization
```python
# Use select_related for foreign keys
reports = ScanReport.objects.select_related('user').all()

# Use prefetch_related for many-to-many
reports = ScanReport.objects.prefetch_related('tags').all()

# Use only() to limit fields
reports = ScanReport.objects.only('url', 'result', 'confidence')
```

### Caching
```python
# scanner/utils.py
from django.core.cache import cache

def predict_phishing(url):
    cache_key = f"prediction_{hash(url)}"
    result = cache.get(cache_key)
    
    if result is None:
        result = run_prediction(url)
        cache.set(cache_key, result, 3600)  # Cache for 1 hour
    
    return result
```

### Async Processing
```python
# scanner/tasks.py
from celery import shared_task

@shared_task
def analyze_url_async(url):
    """Analyze URL asynchronously"""
    result = predict_phishing(url)
    # Save to database
    return result
```

## Security Considerations

### Input Validation
```python
# scanner/forms.py
from django import forms
from django.core.validators import URLValidator

class URLScanForm(forms.Form):
    url = forms.URLField(
        validators=[URLValidator()],
        max_length=500,
        help_text="Enter a valid URL"
    )
    
    def clean_url(self):
        url = self.cleaned_data['url']
        # Additional validation
        if not url.startswith(('http://', 'https://')):
            raise forms.ValidationError("URL must start with http:// or https://")
        return url
```

### Rate Limiting
```python
# scanner/views.py
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='10/m', method='POST')
def analyze_url_view(request):
    # View implementation
    pass
```

## Debugging

### Django Debug Toolbar
```python
# settings/development.py
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    INTERNAL_IPS = ['127.0.0.1']
```

### Logging Configuration
```python
# settings/base.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logs/debug.log',
        },
    },
    'loggers': {
        'scanner': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

### Debugging Tools
```python
# In your code
import pdb; pdb.set_trace()  # Python debugger
import ipdb; ipdb.set_trace()  # Enhanced debugger

# Django shell
python manage.py shell

# Django shell with specific settings
python manage.py shell --settings=phishshield.settings.development
```

## Deployment

### Development Deployment
```bash
# Start development server
python main.py

# Or use Django directly
python manage.py runserver
```

### Production Deployment
```bash
# Collect static files
python manage.py collectstatic

# Run migrations
python manage.py migrate

# Start production server
gunicorn phishshield.wsgi:application
```

### Docker Deployment
```dockerfile
# Dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "main.py"]
```

## Contributing

### Git Workflow
```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "Add new feature"

# Push to remote
git push origin feature/new-feature

# Create pull request
```

### Code Review Checklist
- [ ] Code follows PEP 8 style guide
- [ ] All tests pass
- [ ] New features have tests
- [ ] Documentation is updated
- [ ] No security vulnerabilities
- [ ] Performance considerations addressed

## Troubleshooting

### Common Issues

#### Import Errors
```bash
# Check Python path
python -c "import sys; print(sys.path)"

# Install in development mode
pip install -e .
```

#### Database Issues
```bash
# Reset database
rm db.sqlite3
python manage.py migrate

# Check migrations
python manage.py showmigrations
```

#### Static Files Issues
```bash
# Collect static files
python manage.py collectstatic

# Check static file configuration
python manage.py findstatic styles.css
```

#### Model Issues
```bash
# Check model validation
python manage.py check

# Validate specific app
python manage.py check scanner
```

## Resources

### Documentation
- [Django Documentation](https://docs.djangoproject.com/)
- [Python Documentation](https://docs.python.org/)
- [NumPy Documentation](https://numpy.org/doc/)

### Tools
- [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Celery](https://docs.celeryproject.org/)

### Testing
- [pytest-django](https://pytest-django.readthedocs.io/)
- [Coverage.py](https://coverage.readthedocs.io/)

---

*Last updated: September 2024*
*Developer Setup Guide version: 1.0.0*
