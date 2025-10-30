# PhishShield Architecture Documentation

## System Overview

PhishShield is a Django-based web application that uses Q-Learning AI to detect phishing URLs. The system provides real-time URL analysis, detailed reporting, and PDF export functionality.

## High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Browser   │◄──►│   Django App    │◄──►│   SQLite DB     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │  Q-Learning ML  │
                       │     Model       │
                       └─────────────────┘
```

## Technology Stack

### Backend
- **Framework**: Django 5.2.6
- **Database**: SQLite (development), PostgreSQL (production ready)
- **ML Framework**: NumPy
- **PDF Generation**: ReportLab
- **Python Version**: 3.8+

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with CSS variables
- **JavaScript**: Vanilla JS for interactions
- **Responsive Design**: Mobile-first approach

### Infrastructure
- **Web Server**: Django development server / Gunicorn (production)
- **Static Files**: WhiteNoise for serving
- **Caching**: Redis (production)
- **Logging**: File and console logging

## Component Architecture

### 1. Django Project Structure

```
phishshield/
├── manage.py                 # Django management script
├── main.py                   # Application launcher
├── phishshield/              # Project configuration
│   ├── settings.py           # Django settings
│   ├── urls.py              # Main URL routing
│   └── wsgi.py              # WSGI configuration
├── scanner/                  # Main application
│   ├── models.py            # Data models
│   ├── views.py             # View functions
│   ├── utils.py             # ML utilities
│   ├── admin.py             # Admin interface
│   ├── forms.py             # Form definitions
│   ├── urls.py              # App URL routing
│   └── tests/               # Test suite
├── templates/                # HTML templates
├── static/                   # Static assets
└── docs/                     # Documentation
```

### 2. Data Flow

1. **User Input**: User enters URL in web form
2. **Form Validation**: Django form validates URL format
3. **Feature Extraction**: System extracts 20+ features from URL
4. **ML Processing**: Q-Learning model analyzes features
5. **Result Generation**: Classification and confidence score
6. **Database Storage**: Results saved to database
7. **Response Rendering**: Results displayed to user
8. **PDF Generation**: Optional PDF report creation

### 3. Machine Learning Pipeline

```
URL Input → Feature Extraction → Model Prediction → Result Classification
    ↓              ↓                    ↓                    ↓
Validation   20+ Features        Q-Learning AI        Phishing/Legitimate
```

## Database Schema

### ScanReport Model

| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary key |
| url | URLField | Scanned URL (max 500 chars) |
| result | CharField | 'phishing' or 'legitimate' |
| confidence | FloatField | Confidence score (0.0-1.0) |
| features | JSONField | Extracted features |
| timestamp | DateTimeField | Analysis timestamp |

### Indexes

- `timestamp` - For chronological queries
- `result` - For filtering by classification
- `confidence` - For confidence-based queries
- `url + timestamp` - For URL-specific queries
- `result + confidence` - For combined filtering

## API Endpoints

### Web Interface

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Homepage with URL input form |
| `/result/` | POST | Process URL analysis |
| `/report/<id>/pdf/` | GET | Download PDF report |
| `/admin/` | GET | Django admin interface |

### Request/Response Flow

#### POST /result/
```http
Request:
POST /result/ HTTP/1.1
Content-Type: application/x-www-form-urlencoded

url=https://example.com&csrfmiddlewaretoken=...

Response:
HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
  <!-- Results page with analysis -->
</html>
```

## Security Architecture

### Input Validation
- URL format validation
- Length constraints (max 500 chars)
- XSS protection via template escaping
- CSRF protection on all forms

### Database Security
- Django ORM for SQL injection prevention
- Parameterized queries
- No raw SQL execution

### Session Security
- Secure session cookies (production)
- HTTP-only cookies
- CSRF token validation

## Performance Considerations

### Caching Strategy
- Model predictions cached (1 hour TTL)
- Static files cached
- Database query optimization

### Database Optimization
- Proper indexing on frequently queried fields
- Query optimization with select_related
- Connection pooling (production)

### Static Files
- WhiteNoise for serving static files
- Gzip compression
- CDN ready (production)

## Scalability Design

### Horizontal Scaling
- Stateless application design
- Database connection pooling
- Redis for shared caching
- Load balancer ready

### Vertical Scaling
- Optimized database queries
- Efficient memory usage
- Background task processing ready

## Monitoring and Logging

### Logging Levels
- **DEBUG**: Development debugging
- **INFO**: General information
- **WARNING**: Warning messages
- **ERROR**: Error conditions

### Log Files
- `logs/phishshield.log` - Application logs
- Django logs - Framework logs
- Access logs - Web server logs

## Deployment Architecture

### Development
```
Developer Machine → Django Dev Server → SQLite
```

### Production
```
Load Balancer → Gunicorn → Django → PostgreSQL
                    ↓
                Redis Cache
```

### Docker (Optional)
```
Docker Container → Django → PostgreSQL
```

## Error Handling

### Exception Types
- **ValidationError**: Form validation failures
- **DatabaseError**: Database connection issues
- **MLModelError**: Model loading/prediction failures
- **PDFGenerationError**: Report generation failures

### Fallback Mechanisms
- Rule-based prediction when ML model unavailable
- Graceful degradation for missing features
- User-friendly error messages

## Configuration Management

### Environment Variables
- `DEBUG`: Development mode flag
- `SECRET_KEY`: Django secret key
- `ALLOWED_HOSTS`: Allowed hostnames
- `DATABASE_URL`: Database connection string

### Settings Hierarchy
1. Environment variables
2. Settings file defaults
3. Django defaults

## Testing Architecture

### Test Types
- **Unit Tests**: Individual component testing
- **Integration Tests**: Component interaction testing
- **Model Tests**: Database model testing
- **View Tests**: HTTP request/response testing

### Test Coverage
- Models: 100% coverage
- Views: 100% coverage
- Forms: 100% coverage
- Utils: 100% coverage

## Future Enhancements

### Planned Features
- API endpoints for programmatic access
- Batch URL processing
- Real-time threat intelligence
- Advanced ML models
- User authentication system

### Scalability Improvements
- Microservices architecture
- Message queue integration
- Advanced caching strategies
- Database sharding

---

*Last updated: September 2024*
*Architecture version: 1.0.0*
