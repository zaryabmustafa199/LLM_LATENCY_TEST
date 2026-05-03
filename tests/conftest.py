import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

@pytest.fixture
def client():
    """Fixture for FastAPI TestClient"""
    return TestClient(app)

@pytest.fixture(autouse=True)
def mock_settings(monkeypatch):
    """Ensure tests use a dummy API key"""
    monkeypatch.setattr(settings, "api_key", "test_secure_key_123456789")
    monkeypatch.setattr(settings, "huggingface_token", "dummy_token")
