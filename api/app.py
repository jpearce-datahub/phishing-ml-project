"""
FastAPI service for exposing threat intelligence metrics and ML predictions.
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import pandas as pd
from pathlib import Path
import sys

# Add ml directory to path for imports
sys.path.append(str(Path(__file__).parent.parent / "ml"))
from inference import predict_single_record, load_model
from train import get_feature_importance

app = FastAPI(
    title="Threat Intelligence Metrics API",
    description="API for accessing phishing threat intelligence metrics and ML predictions",
    version="1.0.0"
)

# Load model at startup
try:
    model = load_model()
    print("Model loaded successfully")
except Exception as e:
    print(f"Warning: Could not load model: {e}")
    model = None

class ThreatPredictionRequest(BaseModel):
    """Request model for threat prediction."""
    url_length: int
    num_dots: int
    subdomain_level: int
    path_level: int
    has_https: int
    has_ip_address: int
    num_sensitive_words: int
    has_random_string: int
    hostname_length: int
    path_length: int
    query_length: int
    pct_ext_hyperlinks: float
    pct_ext_resource_urls: float
    abnormal_form_action: int
    iframe_or_frame: int
    missing_title: int
    right_click_disabled: int
    popup_window: int

class ThreatPredictionResponse(BaseModel):
    """Response model for threat prediction."""
    predicted_class: int
    is_phishing: bool
    phishing_probability: float
    legitimate_probability: float
    confidence: float

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "Threat Intelligence Metrics API",
        "version": "1.0.0",
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }

@app.post("/predict", response_model=ThreatPredictionResponse)
async def predict_threat(request: ThreatPredictionRequest):
    """
    Predict if a URL is phishing based on features.
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Convert request to dict
        features = request.dict()
        
        # Make prediction
        result = predict_single_record(features)
        
        return ThreatPredictionResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.get("/metrics/threat-block-rate")
async def get_threat_block_rate(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)")
):
    """
    Get threat block rate metrics.
    In production, this would query the data warehouse.
    """
    # Mock data - in production, query from fact_events or metrics table
    return {
        "metric": "threat_block_rate",
        "period": {
            "start": start_date or "2024-01-01",
            "end": end_date or "2024-01-31"
        },
        "value": 0.85,
        "unit": "percentage",
        "description": "Percentage of threats successfully blocked"
    }

@app.get("/metrics/product-efficacy")
async def get_product_efficacy(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None)
):
    """
    Get product efficacy score.
    """
    return {
        "metric": "product_efficacy_score",
        "period": {
            "start": start_date or "2024-01-01",
            "end": end_date or "2024-01-31"
        },
        "value": 87.5,
        "unit": "score",
        "description": "Overall product efficacy score (0-100)",
        "components": {
            "detection_rate": 85.0,
            "high_severity_catch_rate": 92.0
        }
    }

@app.get("/metrics/user/{user_id}")
async def get_user_metrics(user_id: str):
    """
    Get metrics for a specific user.
    """
    return {
        "user_id": user_id,
        "total_events": 150,
        "phishing_events": 45,
        "phishing_rate": 30.0,
        "report_rate": 88.9,
        "department": "Engineering",
        "region": "US-East"
    }

@app.get("/metrics/threat-intel-summary")
async def get_threat_intel_summary():
    """
    Get threat intelligence summary.
    """
    return {
        "total_threats": 5000,
        "unique_threats": 4500,
        "severity_distribution": {
            "high": 1500,
            "medium": 2000,
            "low": 1500
        },
        "top_indicators": [
            {"indicator": "has_ip_address", "count": 1200},
            {"indicator": "abnormal_form_action", "count": 950},
            {"indicator": "iframe_or_frame", "count": 800}
        ],
        "trend": "increasing"
    }

@app.get("/model/info")
async def get_model_info():
    """
    Get information about the loaded ML model.
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        feature_importance = get_feature_importance(model, 
            [f"feature_{i}" for i in range(model.n_features_)], top_n=10)
        
        return {
            "model_type": "RandomForestClassifier",
            "n_estimators": model.n_estimators,
            "n_features": model.n_features_,
            "top_features": feature_importance
        }
    except Exception as e:
        return {
            "model_type": "RandomForestClassifier",
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

