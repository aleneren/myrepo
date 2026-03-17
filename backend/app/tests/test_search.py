import os
import io
import pytest
import sys
from unittest.mock import patch, MagicMock

os.environ["DB_PATH"] = "data/db.sqlite3"  # Set test database path
sys.modules["app.services.whisper_service"] = (
    MagicMock()
)  # Replace whisper_service with a mock BEFORE importing app

from app import create_app
from app.model.transcriptions import Transcription


# ----------------------------
# Pytest fixture for Flask client
# ----------------------------
@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ----------------------------
# GET /search endpoint
# ----------------------------
def test_search_transcriptions_endpoint(client):
    # Mock database search results
    mock_results = [Transcription(1, "hello.wav", "Hello world", "2024-01-01")]

    # Patch the exact import used in the route
    with patch("app.routes.search.search_transcriptions", return_value=mock_results):
        response = client.get("/search?query=hello")

        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]["filename"] == mock_results[0].filename
        assert response.json[0]["transcription"] == mock_results[0].transcription
        assert response.json[0]["created_at"] == mock_results[0].created_at
