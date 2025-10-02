# rss_fetcher.py
import feedparser
from datetime import datetime

async def fetch_jobs_from_rss(feed_url: str):
    d = feedparser.parse(feed_url)
    jobs = []
    for entry in d.entries:
        job_id = entry.get("id") or entry.get("link")
        posted_date = None
        if entry.get("published_parsed"):
            posted_date = datetime(*entry.published_parsed[:6])
        jobs.append({
            "job_id": job_id,
            "title": entry.get("title"),
            "description": entry.get("summary"),
            "url": entry.get("link"),
            "posted_date": posted_date,
            "raw": dict(entry)
        })
    return jobs
