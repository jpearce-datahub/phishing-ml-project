# API Service

FastAPI service for exposing threat intelligence metrics and ML predictions.

## Endpoints

### Health & Info

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /model/info` - ML model information

### Metrics

- `GET /metrics/threat-block-rate` - Threat block rate metrics
- `GET /metrics/product-efficacy` - Product efficacy score
- `GET /metrics/user/{user_id}` - User-specific metrics
- `GET /metrics/threat-intel-summary` - Threat intelligence summary

### Predictions

- `POST /predict` - Predict if a URL is phishing

## Usage

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app:app --reload
```

### Docker

```bash
# Build and run
docker-compose up --build

# Or build separately
docker build -t phishing-ml-api .
docker run -p 8000:8000 phishing-ml-api
```

### Testing

```bash
pytest tests/
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Example Requests

### Predict Threat

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "url_length": 72,
    "num_dots": 3,
    "subdomain_level": 1,
    "path_level": 5,
    "has_https": 0,
    "has_ip_address": 0,
    "num_sensitive_words": 0,
    "has_random_string": 0,
    "hostname_length": 21,
    "path_length": 44,
    "query_length": 0,
    "pct_ext_hyperlinks": 0.0,
    "pct_ext_resource_urls": 0.25,
    "abnormal_form_action": 0,
    "iframe_or_frame": 0,
    "missing_title": 1,
    "right_click_disabled": 0,
    "popup_window": 0
  }'
```

### Get Metrics

```bash
curl "http://localhost:8000/metrics/threat-block-rate"
curl "http://localhost:8000/metrics/product-efficacy"
curl "http://localhost:8000/metrics/user/user_123"
```

## Configuration

Set environment variables:
- `ENVIRONMENT`: production or development
- `MODEL_PATH`: Path to ML model file

