import json

import groq
from fastapi import HTTPException

from app.config import get_settings
from app.logger import get_logger

MODEL = "llama-3.1-8b-instant"


class GroqService:
    """Service layer for all Groq LLM API interactions."""

    def __init__(self) -> None:
        """Initialize Groq client with API key from environment settings."""
        settings = get_settings()
        self.client = groq.Groq(api_key=settings.GROQ_API_KEY)
        self.model = MODEL
        self.logger = get_logger(__name__)

    # ── Summarize ──────────────────────────────────────────────────────────────

    def summarize(self, text: str, max_length: int, language: str) -> dict:
        """Summarize the given text using the Groq LLM.

        Args:
            text: The input text to summarize.
            max_length: Maximum number of words for the summary.
            language: Language in which the summary should be written.

        Returns:
            A dict with keys: summary, original_length, summary_length, model_used.

        Raises:
            HTTPException: 503 if Groq API is unreachable, 401 for invalid key,
                429 for rate limit exceeded, 502 for other API errors.
        """
        self.logger.info("Summarizing text of length %d", len(text))

        system_prompt = "You are an expert summarizer. Summarize the given text concisely and clearly."
        user_prompt = (
            f"Summarize the following text in {language}, keeping it under {max_length} words. "
            "Return only the summary, no preamble.\n\n"
            f"{text}"
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )
        except groq.APIConnectionError as exc:
            self.logger.error("Groq connection error: %s", exc)
            raise HTTPException(status_code=503, detail="Groq API unreachable") from exc
        except groq.AuthenticationError as exc:
            self.logger.error("Groq authentication error: %s", exc)
            raise HTTPException(status_code=401, detail="Invalid Groq API key") from exc
        except groq.RateLimitError as exc:
            self.logger.error("Groq rate limit error: %s", exc)
            raise HTTPException(status_code=429, detail="Groq rate limit exceeded") from exc
        except groq.APIStatusError as exc:
            self.logger.error("Groq API status error %d: %s", exc.status_code, exc.message)
            raise HTTPException(status_code=502, detail=exc.message) from exc

        summary = response.choices[0].message.content.strip()
        return {
            "summary": summary,
            "original_length": len(text),
            "summary_length": len(summary),
            "model_used": self.model,
        }

    # ── Translate ──────────────────────────────────────────────────────────────

    def translate(self, text: str, source_language: str, target_language: str) -> dict:
        """Translate the given text using the Groq LLM.

        Args:
            text: The input text to translate.
            source_language: Source language, or "auto" for automatic detection.
            target_language: Target language for the translation.

        Returns:
            A dict with keys: translated_text, source_language, target_language, model_used.

        Raises:
            HTTPException: 503 if Groq API is unreachable, 401 for invalid key,
                429 for rate limit exceeded, 502 for other API errors.
        """
        self.logger.info("Translating text to %s", target_language)

        system_prompt = (
            "You are a professional translator. "
            "Translate text accurately while preserving tone and meaning."
        )
        if source_language == "auto":
            user_prompt = (
                f"Detect the language and translate to {target_language}. "
                "Return only the translated text.\n\n"
                f"{text}"
            )
        else:
            user_prompt = (
                f"Translate from {source_language} to {target_language}. "
                "Return only the translated text.\n\n"
                f"{text}"
            )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )
        except groq.APIConnectionError as exc:
            self.logger.error("Groq connection error: %s", exc)
            raise HTTPException(status_code=503, detail="Groq API unreachable") from exc
        except groq.AuthenticationError as exc:
            self.logger.error("Groq authentication error: %s", exc)
            raise HTTPException(status_code=401, detail="Invalid Groq API key") from exc
        except groq.RateLimitError as exc:
            self.logger.error("Groq rate limit error: %s", exc)
            raise HTTPException(status_code=429, detail="Groq rate limit exceeded") from exc
        except groq.APIStatusError as exc:
            self.logger.error("Groq API status error %d: %s", exc.status_code, exc.message)
            raise HTTPException(status_code=502, detail=exc.message) from exc

        translated = response.choices[0].message.content.strip()
        return {
            "translated_text": translated,
            "source_language": source_language,
            "target_language": target_language,
            "model_used": self.model,
        }

    # ── Generate Email ─────────────────────────────────────────────────────────

    def generate_email(
        self,
        context: str,
        tone: str,
        recipient_name: str | None,
        sender_name: str | None,
        email_type: str,
    ) -> dict:
        """Generate a complete email (subject + body) using the Groq LLM.

        Args:
            context: Description of what the email should be about.
            tone: Desired tone (e.g. "professional", "friendly", "formal", "casual").
            recipient_name: Name of the email recipient, or None if not specified.
            sender_name: Name of the email sender, or None if not specified.
            email_type: Category of email (e.g. "general", "follow-up", "apology").

        Returns:
            A dict with keys: subject, body, tone, email_type, model_used.

        Raises:
            HTTPException: 503 if Groq API is unreachable, 401 for invalid key,
                429 for rate limit exceeded, 502 for other API errors,
                500 if the model response cannot be parsed as JSON.
        """
        self.logger.info("Generating %s email with %s tone", email_type, tone)

        system_prompt = (
            "You are an expert email writer. "
            "Write clear, effective emails based on the given context."
        )

        recipient_line = f"Recipient: {recipient_name}" if recipient_name else "Recipient: (not specified)"
        sender_line = f"Sender: {sender_name}" if sender_name else "Sender: (not specified)"

        user_prompt = (
            f"Write a {email_type} email with a {tone} tone.\n"
            f"{recipient_line}\n"
            f"{sender_line}\n"
            f"Context: {context}\n\n"
            'Return ONLY a JSON object with exactly two keys: "subject" and "body". '
            "No markdown, no explanation, just the JSON."
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )
        except groq.APIConnectionError as exc:
            self.logger.error("Groq connection error: %s", exc)
            raise HTTPException(status_code=503, detail="Groq API unreachable") from exc
        except groq.AuthenticationError as exc:
            self.logger.error("Groq authentication error: %s", exc)
            raise HTTPException(status_code=401, detail="Invalid Groq API key") from exc
        except groq.RateLimitError as exc:
            self.logger.error("Groq rate limit error: %s", exc)
            raise HTTPException(status_code=429, detail="Groq rate limit exceeded") from exc
        except groq.APIStatusError as exc:
            self.logger.error("Groq API status error %d: %s", exc.status_code, exc.message)
            raise HTTPException(status_code=502, detail=exc.message) from exc

        raw = response.choices[0].message.content.strip()

        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError as exc:
            self.logger.error("Failed to parse email JSON response: %s", raw)
            raise HTTPException(status_code=500, detail="Failed to parse email response") from exc

        return {
            "subject": parsed["subject"],
            "body": parsed["body"],
            "tone": tone,
            "email_type": email_type,
            "model_used": self.model,
        }


groq_service = GroqService()
