# PhishShield FAQ

## Frequently Asked Questions

This document answers the most common questions about PhishShield.

## General Questions

### What is PhishShield?
PhishShield is a Django-based web application that uses Q-Learning AI to detect phishing URLs. It provides real-time URL analysis, detailed reporting, and PDF export functionality.

### How does PhishShield work?
1. You enter a URL in the web interface
2. The system extracts 20+ features from the URL
3. A trained Q-Learning model analyzes these features
4. The system returns a classification (phishing/legitimate) with confidence score
5. Results are saved to the database and can be downloaded as PDF reports

### Is PhishShield free to use?
Yes, PhishShield is free to use for personal and educational purposes. See the license file for commercial usage terms.

### What types of URLs can PhishShield analyze?
PhishShield can analyze any valid HTTP or HTTPS URL up to 500 characters long. It works with:
- Regular websites
- Shortened URLs
- URLs with query parameters
- URLs with file extensions
- IP addresses

## Technical Questions

### What Python version do I need?
PhishShield requires Python 3.8 or higher. Python 3.9+ is recommended for the best experience.

### What operating systems are supported?
PhishShield works on:
- Windows 10+
- macOS 10.14+
- Linux (Ubuntu 18.04+, CentOS 7+)

### Do I need an internet connection?
No, PhishShield works completely offline. The Q-Learning model is included with the application and doesn't require external API calls.

### What database does PhishShield use?
By default, PhishShield uses SQLite for development. For production, it supports PostgreSQL and MySQL.

### How accurate is PhishShield?
PhishShield's accuracy depends on the training data and model quality. The system includes a fallback rule-based detection system when the ML model is unavailable.

## Installation Questions

### How do I install PhishShield?
1. Clone the repository
2. Create a virtual environment
3. Install dependencies: `pip install -r requirements/development.txt`
4. Run migrations: `python manage.py migrate`
5. Start the server: `python main.py`

### Do I need to install additional ML libraries?
No, all required dependencies are included in the requirements files. The system uses NumPy for ML operations.

### Can I install PhishShield without virtual environment?
While possible, it's not recommended. Virtual environments prevent dependency conflicts and make the system more maintainable.

### How do I update PhishShield?
1. Pull the latest changes: `git pull origin main`
2. Update dependencies: `pip install -r requirements/development.txt --upgrade`
3. Run migrations: `python manage.py migrate`
4. Restart the server

## Usage Questions

### How do I analyze a URL?
1. Open PhishShield in your browser
2. Enter the URL in the input field
3. Click "Analyze URL"
4. View the results and confidence score

### What does the confidence score mean?
The confidence score (0-100%) indicates how certain the system is about its classification:
- 90-100%: Very high confidence
- 70-89%: High confidence
- 50-69%: Medium confidence
- 30-49%: Low confidence
- 0-29%: Very low confidence

### Can I analyze multiple URLs at once?
Currently, PhishShield analyzes one URL at a time. Batch analysis is planned for future versions.

### How do I download PDF reports?
After analyzing a URL, click the "📄 Download PDF Report" button on the results page.

### Can I view analysis history?
Yes, you can view analysis history through the Django admin interface at `/admin/` (requires superuser account).

## Security Questions

### Is my data secure?
Yes, PhishShield includes several security features:
- CSRF protection
- Input validation
- SQL injection prevention
- XSS protection
- Secure session handling

### Are URLs stored permanently?
URLs are stored in the database for analysis history. You can delete old records through the admin interface.

### Can I run PhishShield without internet?
Yes, PhishShield works completely offline and doesn't send data to external servers.

### Is the source code secure?
The source code follows Django security best practices and is regularly reviewed for vulnerabilities.

## Performance Questions

### How fast is PhishShield?
Typical analysis takes 1-3 seconds depending on your system. The system is optimized for speed with caching and efficient algorithms.

### Can PhishShield handle high traffic?
For high traffic, consider:
- Using a production database (PostgreSQL)
- Implementing caching (Redis)
- Using a production web server (Gunicorn)
- Load balancing

### How much memory does PhishShield use?
Memory usage depends on your system and traffic. Typical usage:
- Development: 50-100 MB
- Production: 100-500 MB

### Can I optimize PhishShield for my system?
Yes, you can optimize by:
- Using a faster database
- Enabling caching
- Optimizing static file serving
- Using a CDN

## Development Questions

### Can I contribute to PhishShield?
Yes! Contributions are welcome. See the [Contributing Guide](contributing.md) for details.

### How do I run tests?
```bash
# Run all tests
python manage.py test

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

### How do I add new features?
1. Create a feature branch
2. Implement your changes
3. Add tests
4. Update documentation
5. Submit a pull request

### Can I customize the ML model?
Yes, you can replace the `scanner/model.npy` file with your own trained model. The system expects a specific format (see documentation).

## Troubleshooting Questions

### PhishShield won't start
Check:
1. Python version (3.8+)
2. Dependencies installed
3. Database migrations applied
4. Port 8000 available

### Analysis results seem wrong
This can happen with:
1. Unusual but legitimate URLs
2. New phishing patterns not in training data
3. Edge cases in feature extraction

Use additional verification methods for important decisions.

### PDF reports won't download
Check:
1. ReportLab is installed
2. File permissions
3. Browser PDF viewer settings

### Static files not loading
Run:
```bash
python manage.py collectstatic
```

## Business Questions

### Can I use PhishShield commercially?
Check the license file for commercial usage terms. Some restrictions may apply.

### Is PhishShield suitable for enterprise use?
PhishShield can be used in enterprise environments with proper configuration and security measures.

### Do you provide support?
Community support is available through GitHub issues. Commercial support may be available.

### Can I integrate PhishShield with other systems?
Yes, PhishShield can be integrated with other systems through:
- API endpoints (future)
- Database integration
- Custom Django apps

## Advanced Questions

### How do I train my own model?
1. Collect training data (phishing and legitimate URLs)
2. Extract features using the same method
3. Train a Q-Learning model
4. Save as `scanner/model.npy`

### Can I add new features to the ML model?
Yes, modify the `extract_features()` function in `scanner/utils.py` and retrain the model.

### How do I deploy PhishShield in production?
1. Set up a production database
2. Configure environment variables
3. Use a production web server
4. Set up monitoring and logging
5. Configure security settings

### Can I use PhishShield as a service?
Yes, PhishShield can be deployed as a web service for other applications to use.

## Still Have Questions?

If you can't find the answer to your question:

1. Check the [Troubleshooting Guide](troubleshooting.md)
2. Review the [User Manual](user-manual.md)
3. Search GitHub issues
4. Create a new issue with your question

---

*Last updated: September 2024*
*FAQ version: 1.0.0*
