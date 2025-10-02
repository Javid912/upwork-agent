# Upwork Job Application Agent - Starter Repo

Starter scaffold for an n8n + Playwright + FastAPI system to discover Upwork jobs,
score them, generate proposals (via LLM), run QC, and prepare safe human-in-loop submission.

## Quickstart

1. Copy `.env.example` -> `.env` and fill values (DATABASE_URL, DEEPSEEK_API_KEY).
2. `docker-compose up --build`
3. Initialize DB schema: connect to Postgres and run `sql/schema.sql`.
4. Visit n8n UI: http://localhost:5678
5. Visit FastAPI docs: http://localhost:8000/docs

Notes:
- Replace LLM call in `app/generator.py` with your provider.
- Upwork scraping selectors are placeholders; update them to match Upwork HTML.
