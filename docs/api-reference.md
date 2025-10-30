# PhishShield API Reference

## Overview

This document provides comprehensive API documentation for the PhishShield URL Phishing Detection System. While the current version focuses on web interface usage, this document outlines the API structure for future implementations.

## Base URL

```
Development: http://127.0.0.1:8000
Production: https://your-domain.com
```

## Authentication

Currently, PhishShield does not require authentication for basic URL analysis. Future versions may include API key authentication.

## Endpoints

### 1. Homepage

**GET** `/`

Returns the main application interface with URL input form.

#### Response
```html
HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
  <head>
    <title>PhishShield - URL Phishing Detection</title>
  </head>
  <body>
    <!-- Main application interface -->
  </body>
</html>
```

### 2. URL Analysis

**POST** `/result/`

Analyzes a URL for phishing threats.

#### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `url` | string | Yes | URL to analyze (max 500 characters) |
| `csrfmiddlewaretoken` | string | Yes | CSRF protection token |

#### Request Example
```http
POST /result/ HTTP/1.1
Content-Type: application/x-www-form-urlencoded

url=https://example.com&csrfmiddlewaretoken=abc123...
```

#### Response
```html
HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
  <head>
    <title>PhishShield - Analysis Results</title>
  </head>
  <body>
    <!-- Analysis results page -->
  </body>
</html>
```

#### Error Responses

**400 Bad Request** - Invalid URL format
```html
HTTP/1.1 400 Bad Request
Content-Type: text/html

<!-- Form with validation errors -->
```

**413 Payload Too Large** - URL too long
```html
HTTP/1.1 413 Payload Too Large
Content-Type: text/html

<!-- Error message -->
```

### 3. PDF Report Download

**GET** `/report/{report_id}/pdf/`

Downloads a PDF report for a specific analysis.

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `report_id` | integer | Yes | ID of the scan report |

#### Request Example
```http
GET /report/123/pdf/ HTTP/1.1
```

#### Response
```http
HTTP/1.1 200 OK
Content-Type: application/pdf
Content-Disposition: attachment; filename="phishshield_report_123.pdf"

%PDF-1.4
<!-- PDF content -->
```

#### Error Responses

**404 Not Found** - Report not found
```html
HTTP/1.1 404 Not Found
Content-Type: text/html

<!-- 404 error page -->
```

### 4. Admin Interface

**GET** `/admin/`

Access to Django admin interface for managing scan reports.

#### Authentication
Requires Django superuser account.

#### Response
```html
HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
  <head>
    <title>Django Admin</title>
  </head>
  <body>
    <!-- Django admin interface -->
  </body>
</html>
```

## Data Models

### ScanReport

Represents a URL analysis result.

#### Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Unique identifier |
| `url` | string | Analyzed URL |
| `result` | string | 'phishing' or 'legitimate' |
| `confidence` | float | Confidence score (0.0-1.0) |
| `features` | object | Extracted features (JSON) |
| `timestamp` | datetime | Analysis timestamp |

#### Example
```json
{
  "id": 123,
  "url": "https://example.com",
  "result": "legitimate",
  "confidence": 0.95,
  "features": {
    "url_length": 19,
    "domain_length": 11,
    "is_https": true,
    "has_ip": false,
    "num_dots": 1
  },
  "timestamp": "2024-09-09T12:00:00Z"
}
```

## Feature Extraction

The system extracts 20+ features from each URL for analysis:

### URL Structure Features
- `url_length`: Total URL length
- `domain_length`: Domain name length
- `path_length`: Path component length
- `query_length`: Query string length

### Character Analysis Features
- `num_dots`: Number of dots
- `num_hyphens`: Number of hyphens
- `num_underscores`: Number of underscores
- `num_slashes`: Number of forward slashes
- `num_question_marks`: Number of question marks
- `num_equals`: Number of equals signs
- `num_ampersands`: Number of ampersands
- `num_percent`: Number of percent signs

### Security Indicators
- `is_https`: Whether URL uses HTTPS
- `has_ip`: Whether domain is an IP address
- `has_shortener`: Whether URL uses shortener service
- `has_suspicious_keywords`: Whether URL contains suspicious words

### Domain Analysis
- `subdomain_count`: Number of subdomains
- `has_www`: Whether domain starts with 'www'
- `path_depth`: Depth of URL path
- `has_file_extension`: Whether path has file extension

## Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request - Invalid input |
| 403 | Forbidden - CSRF token missing |
| 404 | Not Found - Resource not found |
| 413 | Payload Too Large - URL too long |
| 500 | Internal Server Error |

## Rate Limiting

Currently, no rate limiting is implemented. Future versions may include:
- 60 requests per minute per IP
- 1000 requests per hour per IP

## CORS Policy

Currently, CORS is not configured. For API access, configure:
```python
CORS_ALLOWED_ORIGINS = [
    "https://your-frontend.com",
]
```

## Future API Endpoints

### Planned Endpoints

#### 1. REST API for Analysis
```http
POST /api/v1/analyze/
Content-Type: application/json

{
  "url": "https://example.com"
}

Response:
{
  "id": 123,
  "url": "https://example.com",
  "result": "legitimate",
  "confidence": 0.95,
  "features": {...},
  "timestamp": "2024-09-09T12:00:00Z"
}
```

#### 2. Batch Analysis
```http
POST /api/v1/analyze/batch/
Content-Type: application/json

{
  "urls": [
    "https://example.com",
    "https://suspicious-site.com"
  ]
}

Response:
{
  "results": [
    {
      "url": "https://example.com",
      "result": "legitimate",
      "confidence": 0.95
    },
    {
      "url": "https://suspicious-site.com",
      "result": "phishing",
      "confidence": 0.87
    }
  ]
}
```

#### 3. Analysis History
```http
GET /api/v1/analyses/
Query Parameters:
- limit: Number of results (default: 50)
- offset: Pagination offset (default: 0)
- result: Filter by result type
- confidence_min: Minimum confidence score

Response:
{
  "count": 1000,
  "next": "http://api.example.com/analyses/?limit=50&offset=50",
  "previous": null,
  "results": [...]
}
```

#### 4. Statistics
```http
GET /api/v1/statistics/

Response:
{
  "total_analyses": 10000,
  "phishing_count": 1500,
  "legitimate_count": 8500,
  "average_confidence": 0.78,
  "analyses_today": 150,
  "top_domains": [
    {"domain": "example.com", "count": 500},
    {"domain": "google.com", "count": 300}
  ]
}
```

## SDK Examples

### Python SDK (Future)
```python
from phishshield import PhishShieldClient

client = PhishShieldClient(api_key="your-api-key")

# Single URL analysis
result = client.analyze("https://example.com")
print(f"Result: {result.result}")
print(f"Confidence: {result.confidence}")

# Batch analysis
results = client.analyze_batch([
    "https://example.com",
    "https://suspicious-site.com"
])

# Get analysis history
history = client.get_analyses(limit=10)
```

### JavaScript SDK (Future)
```javascript
import PhishShieldClient from 'phishshield-js';

const client = new PhishShieldClient('your-api-key');

// Single URL analysis
const result = await client.analyze('https://example.com');
console.log(`Result: ${result.result}`);
console.log(`Confidence: ${result.confidence}`);

// Batch analysis
const results = await client.analyzeBatch([
    'https://example.com',
    'https://suspicious-site.com'
]);
```

## Webhooks (Future)

### Analysis Complete Webhook
```http
POST /webhooks/analysis-complete
Content-Type: application/json
X-PhishShield-Signature: sha256=...

{
  "event": "analysis.complete",
  "data": {
    "id": 123,
    "url": "https://example.com",
    "result": "legitimate",
    "confidence": 0.95,
    "timestamp": "2024-09-09T12:00:00Z"
  }
}
```

## Testing

### Test Endpoints
```bash
# Test homepage
curl http://127.0.0.1:8000/

# Test URL analysis
curl -X POST http://127.0.0.1:8000/result/ \
  -d "url=https://example.com" \
  -H "Content-Type: application/x-www-form-urlencoded"

# Test PDF download
curl http://127.0.0.1:8000/report/1/pdf/ -o report.pdf
```

## Changelog

### Version 1.0.0
- Initial web interface implementation
- URL analysis functionality
- PDF report generation
- Django admin interface

### Future Versions
- REST API endpoints
- Batch processing
- Real-time webhooks
- Advanced analytics

---

*Last updated: September 2024*
*API Reference version: 1.0.0*
