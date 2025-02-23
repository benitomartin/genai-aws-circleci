from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_generate_endpoint():
    response = client.post("/generate", json={"prompt": "Hello, how are you?"})
    assert response.status_code == 200
    assert "generated_text" in response.json()