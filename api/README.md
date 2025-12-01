# Phishing Detection API

FastAPI service for real-time phishing URL detection and threat intelligence metrics.

## Overview

This API provides endpoints for:
- Real-time phishing detection using trained ML models
- Threat intelligence metrics and reporting
- System health monitoring
- Model information and feature importance

## Features

- **Real-time Predictions**: Submit URL features and get instant phishing classification
- **High Performance**: 98%+ accuracy with sub-second response times
- **RESTful Design**: Standard HTTP methods and JSON responses
- **Health Monitoring**: Built-in health checks and status endpoints
- **Docker Support**: Containerized deployment ready

## API Endpoints

### Core Endpoints

- `GET /` - Service information
- `GET /health` - Health check and model status
- `POST /predict` - Phishing detection prediction
- `GET /model/info` - Model information and feature importance

### Metrics Endpoints

- `GET /metrics/threat-block-rate` - Threat blocking statistics
- `GET /metrics/product-efficacy` - Product efficacy scores
- `GET /metrics/user/{user_id}` - User-specific metrics
- `GET /metrics/threat-intel-summary` - Threat intelligence summary

## Request/Response Format

### Prediction Request

```json
{
  "NumDots": 3,
  "SubdomainLevel": 1,
  "PathLevel": 5,
  "UrlLength": 72,
  "NoHttps": 1,
  "IpAddress": 0,
  "PctExtHyperlinks": 0.0,
  "FrequentDomainNameMismatch": 0,
  ...
}
```

### Prediction Response

```json
{
  "predicted_class": 1,
  "is_phishing": true,
  "phishing_probability": 0.95,
  "legitimate_probability": 0.05,
  "confidence": 0.95
}
```

## Running the API

### Local Development

```bash
python app.py
```

The API will be available at `http://localhost:8000`

### Docker Deployment

```bash
docker build -t phishing-api .
docker run -p 8000:8000 phishing-api
```

### Production Deployment

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```

## Dependencies

- FastAPI
- Uvicorn
- Pydantic
- Pandas
- Scikit-learn
- Joblib

## Model Requirements

The API requires a trained model file at `../ml/models/phishing_detection_model_latest.pkl`. Train the model first using the ML training script.

## Testing

Run the test suite:

```bash
pytest tests/
```

## Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`