# PhishShield Troubleshooting Guide

## Common Issues and Solutions

This guide helps you diagnose and resolve common issues with PhishShield.

## Installation Issues

### Python Version Error
**Error**: `❌ Python 3.8 or higher is required`

**Solution**:
1. Check your Python version: `python --version`
2. If Python < 3.8, install Python 3.8+ from [python.org](https://python.org)
3. Ensure Python is in your PATH

### Module Not Found Error
**Error**: `ModuleNotFoundError: No module named 'django'`

**Solution**:
```bash
# Install dependencies
pip install -r requirements/development.txt

# Or use the installation script
python install_requirements.py development
```

### Virtual Environment Issues
**Error**: `venv\Scripts\activate` not found

**Solution**:
```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

## Database Issues

### Database Connection Error
**Error**: `django.db.utils.OperationalError: no such table`

**Solution**:
```bash
# Run migrations
python manage.py migrate

# Check migration status
python manage.py showmigrations
```

### Migration Conflicts
**Error**: `django.db.migrations.exceptions.InconsistentMigrationHistory`

**Solution**:
```bash
# Reset migrations (development only)
rm db.sqlite3
python manage.py migrate

# Or fake the migration
python manage.py migrate --fake-initial
```

### Database Locked
**Error**: `database is locked`

**Solution**:
1. Close any database viewers
2. Restart the Django server
3. Check for long-running queries

## Application Issues

### Server Won't Start
**Error**: `Error: [Errno 98] Address already in use`

**Solution**:
```bash
# Use a different port
python main.py --port 8001

# Or kill the process using port 8000
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### CSRF Verification Failed
**Error**: `CSRF verification failed. Request aborted.`

**Solution**:
1. Ensure `{% csrf_token %}` is in your forms
2. Check if CSRF middleware is enabled
3. Clear browser cookies and try again

### Static Files Not Loading
**Error**: Static files (CSS, JS) not loading

**Solution**:
```bash
# Collect static files
python manage.py collectstatic

# Check static file configuration
python manage.py findstatic styles.css
```

## Model and ML Issues

### Model File Not Found
**Error**: `Q-learning model file not found`

**Solution**:
1. Ensure `scanner/model.npy` exists
2. Check file permissions
3. The system will use rule-based fallback if model is missing

### Model Loading Error
**Error**: `Error loading Q-learning model`

**Solution**:
1. Verify model file is not corrupted
2. Check model file format
3. System will fall back to rule-based prediction

### Prediction Errors
**Error**: `Error in prediction process`

**Solution**:
1. Check URL format is valid
2. Verify all dependencies are installed
3. Check logs for detailed error messages

## Performance Issues

### Slow Response Times
**Symptoms**: Pages load slowly, analysis takes too long

**Solutions**:
1. **Database Optimization**:
   ```bash
   # Check slow queries
   python manage.py shell
   >>> from django.db import connection
   >>> connection.queries
   ```

2. **Enable Caching**:
   ```python
   # settings.py
   CACHES = {
       'default': {
           'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
       }
   }
   ```

3. **Static Files**:
   ```bash
   # Use a CDN or serve static files efficiently
   python manage.py collectstatic
   ```

### Memory Issues
**Error**: `MemoryError` or high memory usage

**Solutions**:
1. Reduce batch sizes
2. Use database pagination
3. Optimize queries with `select_related()`

## Security Issues

### Secret Key Warning
**Warning**: `SECRET_KEY` is not set

**Solution**:
```bash
# Generate a new secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Add to .env file
SECRET_KEY=your-generated-secret-key
```

### Debug Mode in Production
**Warning**: `DEBUG = True` in production

**Solution**:
```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com']
```

### CSRF Issues
**Error**: CSRF token missing or invalid

**Solution**:
1. Ensure CSRF middleware is enabled
2. Include `{% csrf_token %}` in forms
3. Check CSRF cookie settings

## Browser Issues

### JavaScript Not Working
**Symptoms**: Interactive features not working

**Solutions**:
1. Check browser console for errors
2. Ensure JavaScript is enabled
3. Clear browser cache
4. Check static files are loading

### Theme Toggle Not Working
**Symptoms**: Dark/light theme toggle not working

**Solutions**:
1. Check browser supports localStorage
2. Clear browser data
3. Check JavaScript console for errors

### PDF Download Issues
**Error**: PDF not downloading or corrupted

**Solutions**:
1. Check ReportLab is installed: `pip install reportlab`
2. Verify file permissions
3. Check browser PDF viewer settings

## Development Issues

### Test Failures
**Error**: Tests failing unexpectedly

**Solutions**:
```bash
# Run tests with verbose output
python manage.py test -v 2

# Run specific test
python manage.py test scanner.tests.test_models.ScanReportModelTest.test_scan_report_creation

# Check test database
python manage.py test --keepdb
```

### Import Errors
**Error**: `ImportError` or `ModuleNotFoundError`

**Solutions**:
1. Check Python path: `python -c "import sys; print(sys.path)"`
2. Ensure virtual environment is activated
3. Install missing packages: `pip install package-name`

### Migration Issues
**Error**: Migration conflicts or errors

**Solutions**:
```bash
# Check migration status
python manage.py showmigrations

# Create new migration
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Reset migrations (development only)
rm db.sqlite3
python manage.py migrate
```

## Logging and Debugging

### Enable Debug Logging
```python
# settings.py
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

### Check Logs
```bash
# View application logs
tail -f logs/phishshield.log

# Check Django logs
python manage.py shell
>>> import logging
>>> logger = logging.getLogger('scanner')
>>> logger.debug('Test message')
```

### Debug Mode
```python
# Enable debug mode
DEBUG = True

# Add debug toolbar
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
```

## System Requirements

### Minimum Requirements
- Python 3.8+
- 2GB RAM
- 1GB free disk space
- Modern web browser

### Recommended Requirements
- Python 3.9+
- 4GB RAM
- 2GB free disk space
- Chrome, Firefox, or Safari

### Operating System Support
- Windows 10+
- macOS 10.14+
- Linux (Ubuntu 18.04+, CentOS 7+)

## Getting Help

### Self-Help Resources
1. Check this troubleshooting guide
2. Review the [User Manual](user-manual.md)
3. Check the [Developer Setup](developer-setup.md)
4. Review Django documentation

### Community Support
1. Check GitHub issues
2. Search existing discussions
3. Create a new issue with:
   - Error message
   - Steps to reproduce
   - System information
   - Log files

### Professional Support
For enterprise support or custom development:
- Contact the development team
- Check commercial support options

## Error Code Reference

| Error Code | Description | Solution |
|------------|-------------|----------|
| 400 | Bad Request | Check input format |
| 403 | Forbidden | Check CSRF token |
| 404 | Not Found | Check URL path |
| 500 | Internal Server Error | Check logs, restart server |
| 502 | Bad Gateway | Check server configuration |
| 503 | Service Unavailable | Check server status |

## Performance Monitoring

### Database Performance
```python
# Check slow queries
from django.db import connection
print(connection.queries)
```

### Memory Usage
```python
import psutil
import os

process = psutil.Process(os.getpid())
print(f"Memory usage: {process.memory_info().rss / 1024 / 1024:.2f} MB")
```

### Response Times
```python
# Add timing middleware
import time

class TimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time
        print(f"Request took {duration:.2f} seconds")
        return response
```

## Maintenance

### Regular Maintenance Tasks
1. **Database Cleanup**:
   ```bash
   # Remove old scan reports
   python manage.py shell
   >>> from scanner.models import ScanReport
   >>> from datetime import datetime, timedelta
   >>> old_reports = ScanReport.objects.filter(timestamp__lt=datetime.now() - timedelta(days=30))
   >>> old_reports.delete()
   ```

2. **Log Rotation**:
   ```bash
   # Rotate log files
   mv logs/phishshield.log logs/phishshield.log.old
   touch logs/phishshield.log
   ```

3. **Static Files**:
   ```bash
   # Update static files
   python manage.py collectstatic --clear
   ```

### Backup Procedures
1. **Database Backup**:
   ```bash
   # SQLite backup
   cp db.sqlite3 backup/db_$(date +%Y%m%d).sqlite3
   ```

2. **File Backup**:
   ```bash
   # Backup important files
   tar -czf backup/phishshield_$(date +%Y%m%d).tar.gz .
   ```

---

*Last updated: September 2024*
*Troubleshooting Guide version: 1.0.0*
