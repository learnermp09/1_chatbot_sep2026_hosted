import os
import sys

import pytest
from fastapi.testclient import TestClient


# Make the backend folder importable during testing.
BACKEND_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "backend")
)

sys.path.insert(0, BACKEND_DIR)

# Dummy key for CI testing.
# The tests will NOT call the real Groq API.
os.environ["GROQ_API_KEY"] = "test-key"


from main import app  # noqa: E402


client = TestClient(app)


def test_home():
    """Test the root endpoint."""
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "LLM chatbot API is running"
    }


def test_health():
    """Test the health endpoint."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Healthy"
    }


def test_chat(monkeypatch):
    """Test the chat endpoint without calling Groq."""

    def mock_get_response(question):
        return f"Mock response for: {question}"

    monkeypatch.setattr(
        "main.get_response",
        mock_get_response
    )

    response = client.post(
        "/chat",
        json={"message": "What is machine learning?"}
    )

    assert response.status_code == 200

    data = response.json()

    assert "response" in data
    assert data["response"] == (
        "Mock response for: What is machine learning?"
    )


def test_chat_validation():
    """Test validation when message is missing."""

    response = client.post(
        "/chat",
        json={}
    )

    assert response.status_code == 422