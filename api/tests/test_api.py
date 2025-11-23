"""
Tests for the FastAPI application.
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_root():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "service" in response.json()

def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()

def test_threat_block_rate():
    """Test threat block rate endpoint."""
    response = client.get("/metrics/threat-block-rate")
    assert response.status_code == 200
    data = response.json()
    assert "metric" in data
    assert "value" in data

def test_product_efficacy():
    """Test product efficacy endpoint."""
    response = client.get("/metrics/product-efficacy")
    assert response.status_code == 200
    data = response.json()
    assert "metric" in data
    assert "value" in data

def test_user_metrics():
    """Test user metrics endpoint."""
    response = client.get("/metrics/user/user_123")
    assert response.status_code == 200
    data = response.json()
    assert "user_id" in data
    assert "total_events" in data

def test_threat_intel_summary():
    """Test threat intel summary endpoint."""
    response = client.get("/metrics/threat-intel-summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_threats" in data
    assert "severity_distribution" in data

def test_predict_endpoint():
    """Test prediction endpoint."""
    request_data = {
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
    }
    
    response = client.post("/predict", json=request_data)
    # May return 503 if model not loaded, which is acceptable
    assert response.status_code in [200, 503]
    if response.status_code == 200:
        data = response.json()
        assert "predicted_class" in data
        assert "is_phishing" in data

