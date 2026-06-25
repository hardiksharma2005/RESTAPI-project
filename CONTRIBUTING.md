# Contributing

Thank you for considering contributing to AI API Project! This guide covers everything you need to get up and running.

---

## Getting Started

1. **Fork** the repository on GitHub and clone your fork locally:

   ```bash
   git clone https://github.com/<your-username>/ai-api-project.git
   cd ai-api-project
   ```

2. **Create a virtual environment** and activate it:

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS / Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your environment:**

   ```bash
   cp .env.example .env
   # Add your GROQ_API_KEY to .env
   ```

5. **Verify the server starts cleanly:**

   ```bash
   uvicorn app.main:app --reload
   ```

---

## Running Tests

Run the full test suite before submitting any changes:

```bash
pytest tests/test_api.py -v
```

All 9 tests must pass. Do not submit a PR with failing tests.

---

## Code Style

- Follow **PEP 8** for all Python code (4-space indentation, max 100 chars per line).
- Use **descriptive names** — variables, functions, and classes should clearly communicate intent without needing a comment to explain them.
- Add **Google-style docstrings** to all public functions and classes, including `Args`, `Returns`, and `Raises` sections where applicable.
- Keep functions focused on a single responsibility.

---

## Submitting Changes

1. **Create a feature branch** from `main`:

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** and write or update tests as needed.

3. **Commit with a clear, descriptive message:**

   ```bash
   git commit -m "feat: add rate limiting middleware"
   ```

4. **Push your branch** to your fork:

   ```bash
   git push origin feature/your-feature-name
   ```

5. **Open a Pull Request** against the `main` branch. Include:
   - A summary of what changed and why
   - Steps to test the change
   - Screenshots or example responses if applicable
