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
# Test: /transcribe endpoint
# ----------------------------
def test_transcribe_with_audio_file(client):
    # Patch both the whisper service and DB insert
    with patch("app.routes.transcriptions.transcribe_audio") as mock_transcribe, patch(
        "app.routes.transcriptions.insert_transcription"
    ) as mock_insert:

        mock_transcribe.return_value = "Hello world"
        mock_insert.return_value = None  # simulate DB insertion

        data = {"file": (io.BytesIO(b"fake audio data"), "test.wav")}
        response = client.post(
            "/transcribe", data=data, content_type="multipart/form-data"
        )

        assert response.status_code == 200
        assert response.json["transcription"] == "Hello world"
        assert "filename" in response.json


# ----------------------------
# Test: /transcriptions endpoint
# ----------------------------
def test_get_all_transcriptions(client):
    # Mock database response
    mock_transcriptions = [
        Transcription(1, "file1.wav", "First transcription", "2024-01-01"),
        Transcription(2, "file2.wav", "Second transcription", "2024-01-02"),
    ]

    # Patch the exact import used in the route
    with patch(
        "app.routes.transcriptions.get_transcriptions", return_value=mock_transcriptions
    ):
        response = client.get("/transcriptions")

        assert response.status_code == 200
        assert len(response.json) == 2
        assert response.json[0]["transcription"] == "First transcription"
        assert response.json[1]["filename"] == "file2.wav"


# ----------------------------
# Test: /search endpoint
# ----------------------------
def test_search_transcriptions_endpoint(client):
    # Mock database search results
    mock_results = [Transcription(1, "hello.wav", "Hello world", "2024-01-01")]

    # Patch the exact import used in the route
    with patch("app.routes.search.search_transcriptions", return_value=mock_results):
        response = client.get("/search?query=hello")

        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]["transcription"] == "Hello world"
