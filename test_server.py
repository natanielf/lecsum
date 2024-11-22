from fastapi import status
from fastapi.testclient import TestClient

from lecsum import DEFAULT_CONFIG
from server import app

client = TestClient(app)


def test_summary_file_not_found():
    response = client.post(
        "/summarize",
        json={
            "whisper_model": DEFAULT_CONFIG["whisper_model"],
            "ollama_model": DEFAULT_CONFIG["ollama_model"],
            "prompt": DEFAULT_CONFIG["prompt"],
            "file": "not_a_file.mp3",
        },
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_summary():
    response = client.post(
        "/summarize",
        json={
            "whisper_model": DEFAULT_CONFIG["whisper_model"],
            "ollama_model": DEFAULT_CONFIG["ollama_model"],
            "prompt": DEFAULT_CONFIG["prompt"],
            "file": "test/audio.mp3",
        },
    )
    assert response.status_code == status.HTTP_200_OK
