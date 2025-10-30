# PhishShield API Examples

## Base URL
```
https://api.phishshield.com/v1
```

## Authentication
All API requests require an API key in the header:
```
Authorization: Bearer YOUR_API_KEY
```

## Endpoints

### POST /scan
Analyze a URL for phishing threats.

#### Request
```bash
curl -X POST "https://api.phishshield.com/v1/scan" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/login?id=123",
    "options": {
      "include_evidence": true,
      "include_features": true
    }
  }'
```

#### JavaScript Example
```javascript
const response = await fetch('https://api.phishshield.com/v1/scan', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_API_KEY',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    url: 'https://example.com/login?id=123',
    options: {
      include_evidence: true,
      include_features: true
    }
  })
});

const result = await response.json();
console.log(result);
```

#### Python Example
```python
import requests

url = "https://api.phishshield.com/v1/scan"
headers = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}
data = {
    "url": "https://example.com/login?id=123",
    "options": {
        "include_evidence": True,
        "include_features": True
    }
}

response = requests.post(url, headers=headers, json=data)
result = response.json()
print(result)
```

## Response Format

### Success Response (200)
```json
{
  "url": "https://example.com/login?id=123",
  "verdict": "Safe",
  "score": 15,
  "confidence": 0.92,
  "indicators": [
    "Valid SSL certificate",
    "No suspicious keywords detected",
    "Short URL length (acceptable)",
    "Legitimate domain reputation"
  ],
  "recommendation": "This URL appears safe to visit. No security concerns detected.",
  "evidence": {
    "redirect_chain": ["https://example.com/login?id=123"],
    "whois": {
      "registrar": "Example Registrar Inc.",
      "creation_date": "2020-01-15",
      "expiration_date": "2025-01-15"
    },
    "ssl_info": {
      "valid": true,
      "issuer": "Let's Encrypt",
      "expires": "2024-12-31"
    }
  },
  "features": {
    "url_length": 32,
    "domain_length": 11,
    "is_https": true,
    "has_suspicious_keywords": false
  },
  "timestamp": "2024-09-09T16:30:45Z",
  "analysis_time_ms": 1250
}
```

### Error Response (400)
```json
{
  "error": "Invalid URL format",
  "code": "INVALID_URL",
  "message": "The provided URL is not valid. Please check the format and try again."
}
```

### Error Response (429)
```json
{
  "error": "Rate limit exceeded",
  "code": "RATE_LIMIT_EXCEEDED",
  "message": "You have exceeded the rate limit. Please wait before making another request.",
  "retry_after": 60
}
```

## Rate Limits

| Plan | Requests per minute | Requests per day |
|------|-------------------|------------------|
| Free | 10 | 100 |
| Pro | 60 | 10,000 |
| Enterprise | 300 | 100,000 |

## Webhooks

### POST /webhooks/scan-complete
Receive notifications when scan analysis is complete.

#### Payload
```json
{
  "event": "scan.complete",
  "data": {
    "scan_id": "scan_123456789",
    "url": "https://example.com/login?id=123",
    "verdict": "Safe",
    "score": 15,
    "timestamp": "2024-09-09T16:30:45Z"
  }
}
```

## SDKs

### JavaScript/Node.js
```bash
npm install @phishshield/sdk
```

```javascript
import { PhishShield } from '@phishshield/sdk';

const client = new PhishShield('YOUR_API_KEY');
const result = await client.scan('https://example.com/login?id=123');
console.log(result.verdict);
```

### Python
```bash
pip install phishshield-sdk
```

```python
from phishshield import PhishShield

client = PhishShield('YOUR_API_KEY')
result = client.scan('https://example.com/login?id=123')
print(result.verdict)
```

## Integration Examples

### Slack Integration
```javascript
// Slack slash command handler
app.post('/slack/scan', async (req, res) => {
  const url = req.body.text;
  const result = await phishShield.scan(url);
  
  const message = {
    text: `PhishShield Analysis: ${url}`,
    attachments: [{
      color: result.verdict === 'Safe' ? 'good' : 'danger',
      fields: [
        { title: 'Verdict', value: result.verdict, short: true },
        { title: 'Score', value: `${result.score}/100`, short: true },
        { title: 'Recommendation', value: result.recommendation, short: false }
      ]
    }]
  };
  
  res.json(message);
});
```

### SIEM Integration (Splunk)
```python
# Splunk custom command
import requests
import json

def scan_url(url):
    response = requests.post(
        'https://api.phishshield.com/v1/scan',
        headers={'Authorization': 'Bearer YOUR_API_KEY'},
        json={'url': url}
    )
    return response.json()

# Usage in Splunk
url = sys.argv[1]
result = scan_url(url)
print(json.dumps(result))
```
