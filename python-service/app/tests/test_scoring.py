# tests/test_scoring.py
import asyncio
from app.scoring import score_job

def test_score_basic():
    job = {"proposals_count": 3, "client": {"payment_verified": True, "hire_rate": 60}, "hires_count": 0}
    score, reasoning, keys, flags = score_job(job)
    assert isinstance(score, int)
    assert score >= 1 and score <= 10
