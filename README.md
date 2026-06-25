# AI API Project

A production-ready REST API built with FastAPI and powered by Groq's llama-3.1-8b-instant model.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)

---

## Features

- **3 AI-powered endpoints** — text summarization, language translation, and email generation
- **Request validation with Pydantic v2** — strict type checking, field constraints, and auto-generated error messages
- **Structured logging** — timestamped, levelled logs with per-module names and HTTP request/response middleware
- **Environment-based config** — all settings loaded from `.env` via `pydantic-settings`, with a singleton cache
- **Auto-generated API docs** — interactive Swagger UI and ReDoc available out of the box
- **Full test suite** — 9 unit tests with mocked Groq calls using `pytest` and `unittest.mock`

---

## Project Structure

```
ai-api-project/
├── app/
│   ├── __init__.py            # Package marker
│   ├── main.py                # FastAPI app, middleware, lifespan, and root endpoint
│   ├── config.py              # Pydantic-settings config with lru_cache singleton
│   ├── logger.py              # Logging setup — get_logger(name) factory
│   ├── models/
│   │   ├── __init__.py        # Package marker
│   │   └── schemas.py         # Pydantic v2 request/response models for all 3 endpoints
│   ├── routes/
│   │   ├── __init__.py        # Package marker
│   │   ├── summarize.py       # POST /api/v1/summarize/ route
│   │   ├── translate.py       # POST /api/v1/translate/ route
│   │   └── generate_email.py  # POST /api/v1/generate-email/ route
│   └── services/
│       ├── __init__.py        # Package marker
│       └── groq_service.py    # GroqService class + module-level singleton
├── tests/
│   └── test_api.py            # 9 pytest tests covering all endpoints and validation
├── .env.example               # Environment variable template
├── .gitignore                 # Ignores .env, __pycache__, venv, build artefacts
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

---

## Prerequisites

- **Python 3.10+**
- A **Groq API key** — get one free at [https://console.groq.com](https://console.groq.com)

---

## Setup & Installation

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>
   cd ai-api-project
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**

   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS / Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables**

   ```bash
   cp .env.example .env
   ```

   Open `.env` and set your `GROQ_API_KEY`:

   ```
   GROQ_API_KEY=your_actual_key_here
   ```

6. **Run the development server**

   ```bash
   uvicorn app.main:app --reload
   ```

7. **Open the interactive docs**

   Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Environment Variables

| Variable        | Required | Default           | Description                                      |
|-----------------|----------|-------------------|--------------------------------------------------|
| `GROQ_API_KEY`  | Yes      | —                 | Your Groq API key from console.groq.com          |
| `APP_NAME`      | No       | `AI API Project`  | Display name shown in logs and API docs          |
| `APP_VERSION`   | No       | `1.0.0`           | Version string shown in logs and API docs        |
| `DEBUG`         | No       | `False`           | Enable debug mode                                |
| `LOG_LEVEL`     | No       | `INFO`            | Logging level (`DEBUG`, `INFO`, `WARNING`, etc.) |

---

## API Endpoints

### POST /api/v1/summarize/

Summarize a long piece of text into a concise version using AI. Supports multiple output languages.

**Request body**

```json
{
  "text": "Artificial intelligence is transforming industries across the globe...",
  "max_length": 100,
  "language": "english"
}
```

**Response**

```json
{
  "summary": "AI is rapidly transforming global industries by automating tasks and generating insights, though challenges around bias and ethics remain.",
  "original_length": 416,
  "summary_length": 141,
  "model_used": "llama-3.1-8b-instant"
}
```

**Status codes**

| Code | Meaning                              |
|------|--------------------------------------|
| 200  | Text summarized successfully         |
| 422  | Validation error — check request body |
| 429  | Groq rate limit exceeded             |
| 503  | Groq API unreachable                 |

---

### POST /api/v1/translate/

Translate text from one language to another. Set `source_language` to `"auto"` for automatic detection.

**Request body**

```json
{
  "text": "Hello, how are you today?",
  "source_language": "auto",
  "target_language": "french"
}
```

**Response**

```json
{
  "translated_text": "Bonjour, comment allez-vous aujourd'hui?",
  "source_language": "auto",
  "target_language": "french",
  "model_used": "llama-3.1-8b-instant"
}
```

**Status codes**

| Code | Meaning                              |
|------|--------------------------------------|
| 200  | Text translated successfully         |
| 400  | Bad request — invalid language       |
| 422  | Validation error — check request body |
| 429  | Groq rate limit exceeded             |
| 503  | Groq API unreachable                 |

---

### POST /api/v1/generate-email/

Generate a professional email based on context. Supports multiple tones (`professional`, `friendly`, `formal`, `casual`) and email types (`general`, `follow-up`, `apology`, `introduction`, `thank-you`).

**Request body**

```json
{
  "context": "Following up on our meeting last week about the project proposal. Want to check if they have reviewed the documents.",
  "tone": "professional",
  "email_type": "follow-up",
  "recipient_name": "John",
  "sender_name": "Alex"
}
```

**Response**

```json
{
  "subject": "Follow-up on Project Proposal Meeting",
  "body": "Dear John,\n\nI am following up on our meeting last week regarding the project proposal...\n\nBest regards,\nAlex",
  "tone": "professional",
  "email_type": "follow-up",
  "model_used": "llama-3.1-8b-instant"
}
```

**Status codes**

| Code | Meaning                              |
|------|--------------------------------------|
| 200  | Email generated successfully         |
| 422  | Validation error — check request body |
| 429  | Groq rate limit exceeded             |
| 500  | Failed to parse AI response          |
| 503  | Groq API unreachable                 |

---

## Running Tests

```bash
pytest tests/test_api.py -v
```

Expected output:

```
tests/test_api.py::test_root_endpoint                     PASSED  [ 11%]
tests/test_api.py::test_summarize_success                 PASSED  [ 22%]
tests/test_api.py::test_summarize_text_too_short          PASSED  [ 33%]
tests/test_api.py::test_summarize_missing_text            PASSED  [ 44%]
tests/test_api.py::test_translate_success                 PASSED  [ 55%]
tests/test_api.py::test_translate_missing_target_language PASSED  [ 66%]
tests/test_api.py::test_generate_email_success            PASSED  [ 77%]
tests/test_api.py::test_generate_email_invalid_tone       PASSED  [ 88%]
tests/test_api.py::test_generate_email_context_too_short  PASSED  [100%]

======================== 9 passed in 1.39s ========================
```

---

## API Documentation

Once the server is running, interactive documentation is available at:

| Interface       | URL                                     |
|-----------------|-----------------------------------------|
| Swagger UI      | http://127.0.0.1:8000/docs              |
| ReDoc           | http://127.0.0.1:8000/redoc             |
| OpenAPI JSON    | http://127.0.0.1:8000/openapi.json      |

---

## Tech Stack

| Technology      | Version  | Purpose                                      |
|-----------------|----------|----------------------------------------------|
| FastAPI         | 0.100+   | Web framework and OpenAPI generation         |
| Uvicorn         | 0.20+    | ASGI server for running the application      |
| Groq SDK        | 0.11+    | Client library for the Groq inference API    |
| Pydantic v2     | 2.0+     | Data validation and settings management      |
| Python-dotenv   | 1.0+     | `.env` file loading                          |
| Pytest          | 7.0+     | Test framework                               |
