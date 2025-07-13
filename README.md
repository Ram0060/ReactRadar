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
