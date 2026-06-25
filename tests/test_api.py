from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

SUMMARIZE_PATH = "app.services.groq_service.groq_service.summarize"
TRANSLATE_PATH = "app.services.groq_service.groq_service.translate"
GENERATE_EMAIL_PATH = "app.services.groq_service.groq_service.generate_email"

MOCK_SUMMARY = {
    "summary": "Test summary.",
    "original_length": 100,
    "summary_length": 13,
    "model_used": "llama-3.1-8b-instant",
}

MOCK_TRANSLATION = {
    "translated_text": "Hola mundo",
    "source_language": "english",
    "target_language": "spanish",
    "model_used": "llama-3.1-8b-instant",
}

MOCK_EMAIL = {
    "subject": "Test Subject",
    "body": "Test email body.",
    "tone": "professional",
    "email_type": "general",
    "model_used": "llama-3.1-8b-instant",
}


# ── Health Check ───────────────────────────────────────────────────────────────

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "app_name" in data
    assert "version" in data
    assert "status" in data
    assert data["status"] == "running"


# ── Summarize ──────────────────────────────────────────────────────────────────

def test_summarize_success():
    with patch(SUMMARIZE_PATH, return_value=MOCK_SUMMARY):
        response = client.post(
            "/api/v1/summarize/",
            json={"text": "A" * 100, "max_length": 150, "language": "english"},
        )
    assert response.status_code == 200
    assert response.json()["summary"] == "Test summary."


def test_summarize_text_too_short():
    response = client.post("/api/v1/summarize/", json={"text": "short"})
    assert response.status_code == 422


def test_summarize_missing_text():
    response = client.post("/api/v1/summarize/", json={})
    assert response.status_code == 422


# ── Translate ──────────────────────────────────────────────────────────────────

def test_translate_success():
    with patch(TRANSLATE_PATH, return_value=MOCK_TRANSLATION):
        response = client.post(
            "/api/v1/translate/",
            json={"text": "Hello world", "target_language": "spanish"},
        )
    assert response.status_code == 200
    assert response.json()["translated_text"] == "Hola mundo"


def test_translate_missing_target_language():
    response = client.post("/api/v1/translate/", json={"text": "Hello world"})
    assert response.status_code == 422


# ── Generate Email ─────────────────────────────────────────────────────────────

def test_generate_email_success():
    with patch(GENERATE_EMAIL_PATH, return_value=MOCK_EMAIL):
        response = client.post(
            "/api/v1/generate-email/",
            json={"context": "Following up on our meeting last week about the project proposal"},
        )
    assert response.status_code == 200
    data = response.json()
    assert data["subject"] == "Test Subject"
    assert data["tone"] == "professional"


def test_generate_email_invalid_tone():
    response = client.post(
        "/api/v1/generate-email/",
        json={"context": "Following up on our meeting", "tone": "aggressive"},
    )
    assert response.status_code == 422


def test_generate_email_context_too_short():
    response = client.post("/api/v1/generate-email/", json={"context": "Hi"})
    assert response.status_code == 422
