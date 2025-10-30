# PhishShield User Manual

This manual provides comprehensive guidance on using PhishShield for URL phishing detection.

## 🎯 Overview

PhishShield is an AI-powered web application that analyzes URLs to detect potential phishing threats. It uses advanced machine learning algorithms to provide accurate and reliable phishing detection.

## 🚀 Getting Started

### Accessing PhishShield

1. **Open your web browser**
2. **Navigate to** `http://127.0.0.1:8000` (or your configured URL)
3. **You'll see the PhishShield homepage**

### First Time Setup

No special setup is required for basic usage. The system is ready to use immediately after installation.

## 🔍 Using PhishShield

### Analyzing a URL

1. **Enter the URL** you want to analyze in the input field
2. **Click "Analyze URL"** button
3. **Wait for analysis** to complete (usually takes 1-3 seconds)
4. **Review the results** displayed on the results page

### Understanding Results

#### Result Types

- **✅ LEGITIMATE URL**: The URL appears to be safe
- **⚠️ PHISHING DETECTED**: The URL shows signs of being a phishing attempt

#### Confidence Score

The confidence score indicates how certain the system is about its analysis:

- **90-100%**: Very high confidence
- **70-89%**: High confidence
- **50-69%**: Medium confidence
- **30-49%**: Low confidence
- **0-29%**: Very low confidence

#### Feature Analysis

The system analyzes various URL features:

**URL Structure**
- URL Length: Total number of characters
- Domain Length: Length of the domain name
- Path Length: Length of the URL path
- Query Length: Length of query parameters

**Character Analysis**
- Dots: Number of dots in the URL
- Hyphens: Number of hyphens
- Underscores: Number of underscores
- Slashes: Number of forward slashes

**Security Indicators**
- HTTPS: Whether the URL uses secure HTTPS
- IP Address: Whether the domain is an IP address
- URL Shortener: Whether the URL uses a shortener service
- Suspicious Keywords: Whether the URL contains suspicious words

### Downloading Reports

1. **After analysis**, click "📄 Download PDF Report"
2. **The PDF will download** to your default download folder
3. **Open the PDF** to view detailed analysis results

## 🎨 Interface Features

### Theme Toggle

- **Click the theme toggle button** (🌙/☀️) in the top-right corner
- **Switch between light and dark themes**
- **Your preference is saved** for future visits

### Responsive Design

- **Works on all devices**: Desktop, tablet, and mobile
- **Touch-friendly**: Optimized for touch screens
- **Accessible**: Follows web accessibility guidelines

## 🔧 Advanced Usage

### Batch Analysis

While PhishShield doesn't currently support batch analysis through the web interface, you can:

1. **Analyze multiple URLs** one by one
2. **Download individual reports** for each analysis
3. **Keep track of results** using the report IDs

### API Usage (Future Feature)

Future versions will include API endpoints for programmatic access:

```python
# Example (future feature)
import requests

response = requests.post('http://localhost:8000/api/analyze/', {
    'url': 'https://example.com'
})
result = response.json()
```

## 📊 Understanding the Analysis

### How PhishShield Works

1. **Feature Extraction**: The system extracts 20+ features from the URL
2. **AI Analysis**: A trained Q-Learning model analyzes the features
3. **Risk Assessment**: The system calculates a risk score
4. **Result Generation**: A final classification and confidence score are generated

### What Makes a URL Suspicious?

Common indicators of phishing URLs:

- **IP addresses instead of domain names**
- **URL shorteners** (bit.ly, tinyurl.com, etc.)
- **Suspicious keywords** (secure, account, update, verify, etc.)
- **Unusual character patterns**
- **Long URLs with many parameters**
- **Missing HTTPS encryption**
- **Multiple subdomains**

### Accuracy and Limitations

- **High accuracy** on common phishing patterns
- **May have false positives** on legitimate but unusual URLs
- **Regularly updated** with new threat patterns
- **Best used as one tool** in a comprehensive security strategy

## 🛡️ Security Best Practices

### When to Use PhishShield

- **Before clicking suspicious links** in emails
- **Verifying URLs** from unknown sources
- **Checking shortened URLs** before visiting
- **Validating links** in social media posts

### Additional Security Measures

- **Keep your browser updated**
- **Use antivirus software**
- **Be cautious with email attachments**
- **Verify sender identities**
- **Use two-factor authentication**

## 🐛 Troubleshooting

### Common Issues

#### "URL is too long" Error
- **Problem**: URL exceeds 500 character limit
- **Solution**: Use a URL shortener or contact the URL owner

#### "Invalid URL" Error
- **Problem**: URL format is incorrect
- **Solution**: Ensure URL starts with http:// or https://

#### Analysis Takes Too Long
- **Problem**: Analysis is taking more than 30 seconds
- **Solution**: Refresh the page and try again

#### Results Seem Incorrect
- **Problem**: Legitimate URL marked as phishing
- **Solution**: This can happen with unusual but legitimate URLs. Use additional verification methods.

### Getting Help

If you encounter issues:

1. **Check the troubleshooting guide**
2. **Verify your internet connection**
3. **Try a different browser**
4. **Contact support** if problems persist

## 📈 Tips for Better Results

### URL Format
- **Use complete URLs** including http:// or https://
- **Avoid truncated URLs** when possible
- **Include the full path** for better analysis

### Understanding Confidence Scores
- **High confidence (80%+)**: Very reliable result
- **Medium confidence (50-79%)**: Good result, but verify
- **Low confidence (<50%)**: Use additional verification

### Regular Updates
- **Keep PhishShield updated** for the latest threat patterns
- **Check for updates** regularly
- **Report false positives** to help improve the system

## 🔄 Updates and Maintenance

### Automatic Updates
- **No automatic updates** currently available
- **Manual updates** required
- **Check for updates** regularly

### Data Privacy
- **URLs are analyzed locally** when possible
- **No personal data is stored** unless you choose to save reports
- **Analysis results** are stored temporarily for report generation

## 📞 Support and Feedback

### Getting Support
- **Check the FAQ** for common questions
- **Review troubleshooting guides**
- **Open an issue** on the project repository

### Providing Feedback
- **Report bugs** through the issue tracker
- **Suggest improvements** via pull requests
- **Share your experience** with the community

---

*Last updated: September 2024*
*User Manual version: 1.0.0*
