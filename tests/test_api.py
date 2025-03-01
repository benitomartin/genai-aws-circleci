from fastapi.testclient import TestClient
from main import app
import pytest
import os

@pytest.fixture
def client():
    """Fixture for FastAPI test client"""
    return TestClient(app)

def test_root(client):
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the GenAI API"}


def test_generate_text(client):
    """Test the generate endpoint"""
    
    # Test with a sample prompt
    response = client.post("/generate", json={"prompt": "Tell me a joke"})
    
    # Assert the status code and the response content
    assert response.status_code == 200
    assert "response" in response.json()
