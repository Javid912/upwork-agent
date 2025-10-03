# main.py
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.fetcher.rss_fetcher import fetch_jobs_from_rss
from app.fetcher.playwright_fetcher import fetch_jobs_with_playwright
from app.db import Database
from app.scoring import score_job
from app.generator import generate_proposal_text
from app.qc import run_qc

class FetchPlaywrightRequest(BaseModel):
    query: str
    pages: int = 1

app = FastAPI(title="Upwork Agent Service")
db = Database()

@app.get("/")
async def root():
    return {"message": "Upwork Agent Service", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "upwork-agent"}

@app.on_event("startup")
async def startup():
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()

@app.post("/fetch/rss")
async def fetch_rss(feed_url: str):
    jobs = await fetch_jobs_from_rss(feed_url)
    inserted = []
    for job in jobs:
        await db.upsert_job(job)
        inserted.append(job["job_id"])
    return {"inserted": inserted, "count": len(jobs)}

@app.post("/fetch/playwright")
async def fetch_playwright(request: FetchPlaywrightRequest):
    try:
        jobs = await fetch_jobs_with_playwright(request.query, pages=request.pages)
        inserted = []
        for job in jobs:
            await db.upsert_job(job)
            inserted.append(job["job_id"])
        return {"inserted": inserted, "count": len(jobs)}
    except Exception as e:
        print(f"Error in fetch_playwright endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch jobs: {str(e)}")

@app.post("/analyze/{job_id}")
async def analyze_job(job_id: str):
    job = await db.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="job not found")
    score, reasoning, key_requirements, flags = score_job(job)
    await db.upsert_scored_job(job_id, score, reasoning, key_requirements, flags)
    return {"job_id": job_id, "score": score, "reasoning": reasoning}

@app.post("/generate/{job_id}")
async def generate(job_id: str):
    job = await db.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="job not found")
    proposal_text = await generate_proposal_text(job)
    qc_ok, qc_issues = await run_qc(job, proposal_text)
    await db.insert_proposal(job_id, proposal_text, qc_ok, qc_issues, status="pending")
    return {"job_id": job_id, "qc_passed": qc_ok, "issues": qc_issues, "proposal": proposal_text}

@app.post("/prepare_submission/{job_id}")
async def prepare_submission(job_id: str):
    job = await db.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="job not found")
    proposal = await db.get_latest_proposal(job_id)
    return {
        "job_url": job.get("url"),
        "prefill_text": proposal["proposal_text"] if proposal else ""
    }
