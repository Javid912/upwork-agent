# generator.py
import os, httpx

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")

FEW_SHOT_EXAMPLES = [
    {"job_snippet": "Scrape product list & export CSV monthly", "proposal": "I will build a scheduled scraper..."},
    {"job_snippet": "Exhibitor directory scrape + dashboard", "proposal": "I will scrape, dedupe and deliver a dashboard..."}
]

async def call_llm(prompt: str) -> str:
    # TODO: Replace with your provider call.
    # Example: call a dummy echo for now to keep things local-testable.
    # On production, replace with DeepSeek/OpenAI call (use DEEPSEEK_API_KEY).
    return "DUMMY PROPOSAL: " + prompt[:800]  # quick stub

async def generate_proposal_text(job: dict) -> str:
    profile = (
        "Javad Satoungar — Junior Data Engineer / ETL Developer, 4+ years. "
        "Skills: Playwright, Scrapy, Python, Postgres. "
        "Deliverables: clean CSV, scheduled updates, documented code."
    )
    prompt = f"{profile}\n\nJob:\n{job.get('title')} - {job.get('description')}\n\nExamples:\n"
    for ex in FEW_SHOT_EXAMPLES:
        prompt += f"Job: {ex['job_snippet']}\nProposal: {ex['proposal']}\n\n"
    prompt += "\nNow write a concise (180-250 word) proposal emphasizing reliability, maintainability, and willingness to deliver a demo."
    return await call_llm(prompt)
