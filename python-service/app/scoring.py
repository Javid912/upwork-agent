# scoring.py
from datetime import datetime, timezone

def time_since_posted_weight(posted_date):
    if not posted_date:
        return 0
    delta = datetime.now(timezone.utc) - posted_date
    hours = delta.total_seconds()/3600
    if hours < 2:
        return 2
    if hours < 12:
        return 1
    if hours > 168:
        return -2
    return 0

def score_job(job: dict):
    score = 5
    flags = []
    key_reqs = []

    prop = job.get("proposals_count") or 0
    if prop < 10:
        score += 2
    elif 10 <= prop <= 15:
        score += 1
    elif 15 < prop <= 20:
        score -= 1
    else:
        score -= 3

    if job.get("client", {}).get("payment_verified"):
        score += 1

    hire_rate = job.get("client", {}).get("hire_rate") or 0
    if hire_rate > 50:
        score += 1

    if job.get("last_viewed"):
        score += 1

    budget = job.get("budget_amount") or 0
    if budget and budget < 50:
        score -= 2

    posted_date = job.get("posted_date")
    score += time_since_posted_weight(posted_date)

    desc = (job.get("description") or "") + " " + (job.get("title") or "")
    niche = any(k in desc.lower() for k in ["treasury", "legal", "financial", "market research", "treasury bonds"])
    if niche:
        score += 1
        key_reqs.append("niche")

    if job.get("hires_count", 0) > 0:
        score -= 1

    score = max(1, min(10, score))
    reasoning = f"Computed score {score}: proposals={prop}, payment_verified={job.get('client',{}).get('payment_verified')}, hire_rate={hire_rate}"
    return int(score), reasoning, key_reqs, flags
