from fastapi.testclient import TestClient
from fastapi import HTTPException
from unittest.mock import patch, MagicMock
from main import app
import pytest
import os

@pytest.fixture
def client():
    """Fixture for FastAPI test client"""
    return TestClient(app)

def test_root_endpoint(client):
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the GenAI API"}

def test_generate_endpoint(client):
    """Test the generate endpoint"""

    response = client.post("/generate", json={"prompt": "Tell me a joke"})

    # Assert error status code
    response_data = response.json()
    assert response.status_code == 200
    assert "response" in response_data
    assert isinstance(response_data["response"], str)
    assert len(response_data["response"]) > 0

def test_generate_invalid_input(client):
    """Test the generate endpoint with invalid input"""
    # Test with missing prompt field
    response = client.post("/generate", json={})

    # Assert validation error
    assert response.status_code == 422 # Unprocessable Entity
    assert "prompt" in response.json()["detail"][0]["loc"]

@patch("main.get_openai_api_key") # Patch the get_openai_api_key function in main.py
def test_generate_text_missing_api_key(mock_get_api_key, client):
    """Test the generate endpoint when the API key is missing"""


    # Setup mock to raise an HTTPException
    mock_get_api_key.side_effect = HTTPException(status_code=500, detail="API key not found")

    # Test with a sample prompt
    response = client.post("/generate", json={"prompt": "Tell me a joke"})

    # Assert error status code
    assert response.status_code == 500 # Internal Server Error
    assert "API key not found" in response.json()["detail"]

# # Test function to mock OpenAI client behavior
@patch("main.get_openai_client")  # Patch the get_openai_client function in main.py
def test_mock_client(mock_get_client):
    """Test the OpenAI client behavior with a simplified mock client"""

    # Set up the mock OpenAI client and the mock response in one go
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(
            message=MagicMock(content="Mock response")  # Directly mock the message and its content
        )
    ]

    # When `chat.completions.create()` is called, return the mock response
    mock_get_client.return_value.chat.completions.create.return_value = mock_response

    # Simulate calling the OpenAI client's `chat.completions.create()`
    result = mock_get_client.return_value.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Tell me a joke"}],
        max_tokens=200
    )

    # Assert the mock response
    assert result == mock_response
    assert result.choices[0].message.content == "Mock response"

@patch("boto3.session.Session")
def test_get_openai_api_key_aws_environment(mock_session, client):
    """Test retrieving API key from AWS Secrets Manager"""
    
    # Set up environment to simulate AWS Lambda
    with patch.dict(os.environ, {"AWS_LAMBDA_FUNCTION_NAME": "test-function"}, clear=True):
        
        # Create mock for the entire boto3 session and client chain
        mock_client = MagicMock()
        mock_session.return_value.client.return_value = mock_client
        
        # Mock the get_secret_value response
        mock_response = {
            'SecretString': '{"OPENAI_API_KEY": "test-api-key"}'
        }
        mock_client.get_secret_value.return_value = mock_response
        
        # Call the function under test
        from main import get_openai_api_key
        api_key = get_openai_api_key()
        
        # Assertions
        mock_session.assert_called_once()
        mock_session.return_value.client.assert_called_with(
            service_name='secretsmanager', 
            region_name="eu-central-1"
        )
        mock_client.get_secret_value.assert_called_with(SecretId="openai/api_key")
        assert api_key == "test-api-key"