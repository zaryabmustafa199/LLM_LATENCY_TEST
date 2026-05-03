import pytest
from app.config import settings

def test_root_endpoint(client):
    """Test the root endpoint for health and version info"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "llama" in data["models"]

def test_health_endpoint(client):
    """Test the /health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "llama" in data["models"]

def test_generate_endpoint_unauthorized(client):
    """Test /generate with invalid API key"""
    payload = {
        "model": "llama",
        "query": "test"
    }
    headers = {
        "x-api-key": "wrong_but_long_key_123456"
    }
    response = client.post("/generate", json=payload, headers=headers)
    assert response.status_code == 401
    assert "Invalid or missing API Key" in response.json()["detail"]

def test_generate_endpoint_validation_error(client):
    """Test /generate with invalid model (should trigger 422)"""
    payload = {
        "model": "unknown-model",
        "query": "test"
    }
    headers = {
        "x-api-key": "test_secure_key_123456789"
    }
    response = client.post("/generate", json=payload, headers=headers)
    assert response.status_code == 422

