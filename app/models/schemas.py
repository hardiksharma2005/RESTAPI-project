from typing import Literal, Optional
from pydantic import BaseModel, ConfigDict, Field


# ── Summarize ──────────────────────────────────────────────────────────────────

class SummarizeRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=50,
        max_length=10_000,
        description="The text to summarize (50–10,000 characters).",
    )
    max_length: Optional[int] = Field(
        150,
        ge=50,
        le=500,
        description="Maximum word count for the summary (50–500).",
    )
    language: Optional[str] = Field(
        "english",
        description="Language in which the summary should be written.",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "text": (
                    "Artificial intelligence is transforming industries worldwide. "
                    "From healthcare to finance, AI systems are automating complex tasks, "
                    "improving accuracy, and enabling new capabilities that were previously "
                    "impossible. This rapid adoption raises important questions about ethics, "
                    "employment, and the future of human-machine collaboration."
                ),
                "max_length": 100,
                "language": "english",
            }
        }
    )


class SummarizeResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    summary: str = Field(..., description="The generated summary.")
    original_length: int = Field(..., description="Character count of the original input.")
    summary_length: int = Field(..., description="Character count of the summary.")
    model_used: str = Field(..., description="The Groq model used to generate the summary.")


# ── Translate ──────────────────────────────────────────────────────────────────

class TranslateRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=5_000,
        description="The text to translate (1–5,000 characters).",
    )
    source_language: Optional[str] = Field(
        "auto",
        description='Source language. Use "auto" to auto-detect.',
    )
    target_language: str = Field(
        ...,
        description="Target language for the translation (required).",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "text": "Hello, how are you?",
                "source_language": "auto",
                "target_language": "Spanish",
            }
        }
    )


class TranslateResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    translated_text: str = Field(..., description="The translated text.")
    source_language: str = Field(..., description="Detected or specified source language.")
    target_language: str = Field(..., description="Target language of the translation.")
    model_used: str = Field(..., description="The Groq model used for translation.")


# ── Generate Email ─────────────────────────────────────────────────────────────

class GenerateEmailRequest(BaseModel):
    context: str = Field(
        ...,
        min_length=10,
        max_length=2_000,
        description="Description of what the email should be about (10–2,000 characters).",
    )
    tone: Optional[Literal["professional", "friendly", "formal", "casual"]] = Field(
        "professional",
        description="Desired tone of the email.",
    )
    recipient_name: Optional[str] = Field(
        None,
        description="Name of the email recipient (optional).",
    )
    sender_name: Optional[str] = Field(
        None,
        description="Name of the email sender (optional).",
    )
    email_type: Optional[
        Literal["general", "follow-up", "apology", "introduction", "thank-you"]
    ] = Field(
        "general",
        description="Type/category of the email.",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "context": "Following up on the project proposal sent last week and asking for feedback.",
                "tone": "professional",
                "recipient_name": "Jane Smith",
                "sender_name": "John Doe",
                "email_type": "follow-up",
            }
        }
    )


class GenerateEmailResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    subject: str = Field(..., description="Generated email subject line.")
    body: str = Field(..., description="Generated email body.")
    tone: str = Field(..., description="Tone applied to the email.")
    email_type: str = Field(..., description="Type/category of the generated email.")
    model_used: str = Field(..., description="The Groq model used to generate the email.")


# ── Generic Error ──────────────────────────────────────────────────────────────

class ErrorResponse(BaseModel):
    error: str = Field(..., description="Short error message.")
    detail: Optional[str] = Field(None, description="Additional error detail.")
    status_code: int = Field(..., description="HTTP status code.")
