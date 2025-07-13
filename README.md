# ReactRadar FastAPI API

A comprehensive REST API for the ReactRadar brand analysis system, providing endpoints for brand extraction, sentiment analysis, segmentation, and insights generation.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd api
pip install -r requirements.txt
```

### 2. Start the Server
```bash
# Using the startup script
python start_server.py

# Or directly with uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Access the API
- **API Documentation**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📋 API Endpoints

### Core Analysis Endpoints

#### `POST /analyze`
Analyze a transcript and extract comprehensive brand insights.

**Request Body:**
```json
{
  "transcript": "Your transcript text here...",
  "save_results": true
}
```

**Response:**
```json
{
  "success": true,
  "message": "Analysis complete. Found 5 brands.",
  "data": {
    "brands": ["Brand1", "Brand2", "Brand3"],
    "summary": {
      "total_brands_analyzed": 5,
      "average_rating": 4.2
    },
    "brand_insights": [...],
    "comparative_insights": {...}
  }
}
```

#### `GET /brand/{brand_name}`
Analyze a single brand in detail.

**Parameters:**
- `brand_name`: Name of the brand to analyze
- `transcript` (optional): Custom transcript text

**Response:**
```json
{
  "success": true,
  "message": "Analysis complete for My Protein",
  "data": {
    "brand": "My Protein",
    "sentiment_analysis": {
      "avg_rating": 4.5,
      "avg_score": 0.75
    },
    "segmentation": {
      "price_category": "budget",
      "quality_category": "standard"
    },
    "insights": {...}
  }
}
```

#### `POST /compare`
Compare multiple brands side by side.

**Request Body:**
```json
{
  "brands": ["Brand1", "Brand2", "Brand3"],
  "transcript": "Optional transcript text..."
}
```

### Utility Endpoints

#### `POST /extract-brands`
Extract brand names from text.

**Request Body:**
```json
{
  "transcript": "Text containing brand mentions...",
  "known_brands": ["Brand1", "Brand2"]
}
```

#### `POST /sentiment`
Analyze sentiment for specific statements.

**Request Body:**
```json
{
  "brand": "My Protein",
  "statements": [
    "This product is excellent",
    "Great value for money"
  ]
}
```

#### `GET /segments`
Get all brand segments from saved data.

#### `GET /insights`
Get all brand insights from saved data.

#### `GET /files`
List all available data files.

#### `GET /stats`
Get overall system statistics.

#### `POST /upload-transcript`
Upload a JSON file with transcript data.

### System Endpoints

#### `GET /`
Root endpoint with API information.

#### `GET /health`
Health check endpoint.

## 🔧 Usage Examples

### Using Python Requests

```python
import requests

# Initialize client
base_url = "http://localhost:8000"

# Analyze transcript
response = requests.post(f"{base_url}/analyze", json={
    "transcript": "My Protein offers great value...",
    "save_results": True
})
result = response.json()

# Get single brand analysis
response = requests.get(f"{base_url}/brand/My Protein")
brand_data = response.json()

# Compare brands
response = requests.post(f"{base_url}/compare", json={
    "brands": ["My Protein", "Optimum Nutrition"]
})
comparison = response.json()
```

### Using the Test Client

```python
from test_client import ReactRadarClient

# Initialize client
client = ReactRadarClient("http://localhost:8000")

# Health check
health = client.health_check()

# Analyze transcript
result = client.analyze_transcript("Your transcript here...")

# Get insights
insights = client.get_insights()
```

### Using cURL

```bash
# Health check
curl http://localhost:8000/health

# Analyze transcript
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"transcript": "My Protein is excellent...", "save_results": true}'

# Get brand analysis
curl http://localhost:8000/brand/My%20Protein

# Compare brands
curl -X POST http://localhost:8000/compare \
  -H "Content-Type: application/json" \
  -d '{"brands": ["My Protein", "Optimum Nutrition"]}'
```

## 📊 Response Format

All API responses follow a consistent format:

```json
{
  "success": boolean,
  "message": "Human-readable message",
  "data": {
    // Response-specific data
  }
}
```

### Error Responses

```json
{
  "detail": "Error message describing what went wrong"
}
```

## 🛠️ Configuration

### Environment Variables

You can configure the API using environment variables:

```bash
export REACT_RADAR_DATA_DIR="experiment"
export REACT_RADAR_HOST="0.0.0.0"
export REACT_RADAR_PORT="8000"
```

### Server Options

```bash
# Start with custom host and port
python start_server.py --host 127.0.0.1 --port 9000

# Disable auto-reload for production
python start_server.py --no-reload
```

## 🔒 Security

### CORS Configuration

The API includes CORS middleware configured to allow all origins. For production, you should configure specific origins:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

### Rate Limiting

For production deployments, consider adding rate limiting:

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
```

## 🧪 Testing

### Run the Test Client

```bash
python test_client.py
```

### Manual Testing

1. Start the server: `python start_server.py`
2. Open http://localhost:8000/docs
3. Use the interactive Swagger UI to test endpoints

### Automated Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest test_api.py
```

## 📈 Monitoring

### Health Check

Monitor API health with the `/health` endpoint:

```bash
curl http://localhost:8000/health
```

### Statistics

Get system statistics with the `/stats` endpoint:

```bash
curl http://localhost:8000/stats
```

## 🚀 Deployment

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Production Deployment

For production, use a production ASGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 🔧 Troubleshooting

### Common Issues

1. **Import Errors**: Make sure the `src` directory is in the Python path
2. **Data Not Found**: Ensure the `experiment` directory contains required JSON files
3. **Port Already in Use**: Change the port with `--port 8001`

### Debug Mode

Enable debug logging:

```bash
uvicorn main:app --log-level debug
```

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [ReactRadar Core System](../README.md)
- [API Examples](test_client.py)

---

**ReactRadar API** - Transform text into brand intelligence via REST API 🎯 