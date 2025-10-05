# parser.py
import re
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from typing import Dict, List, Optional

def parse_int_from_text(text: Optional[str]) -> int:
    if not text:
        return 0
    m = re.search(r"\d+", text.replace(",", ""))
    return int(m.group()) if m else 0

def parse_money(text: Optional[str]) -> float:
    if not text:
        return 0.0
    # simple extract first number, allow commas and decimals
    m = re.search(r"[\d,]+(?:\.\d+)?", text.replace(",", ""))
    return float(m.group()) if m else 0.0

def parse_posted_date(text: Optional[str]) -> Optional[datetime]:
    if not text:
        return None
    text = text.strip().lower()
    # handle "1 hour ago", "2 days ago", "Posted 3 days ago", "Posted today"
    if "hour" in text or "minute" in text:
        return datetime.now(timezone.utc)
    m = re.search(r"(\d+)\s+day", text)
    if m:
        days = int(m.group(1))
        return datetime.now(timezone.utc) - timedelta(days=days)
    # fallback: try parsing ISO-ish
    try:
        return datetime.fromisoformat(text)
    except Exception:
        return None

def job_from_card_html(html: str) -> Dict:
    """
    Convert a single job-card HTML snippet into the canonical job dict.
    Keep selectors flexible: try multiple candidates.
    """
    s = BeautifulSoup(html, "lxml")

    def first(selector_list: List[str]):
        for sel in selector_list:
            el = s.select_one(sel)
            if el:
                return el.get_text(separator=" ", strip=True)
        return None

    title = first(["h4", "h3", ".job-title", ".jobCard-title", "a.job-title"])
    url_el = s.select_one("a")
    url = url_el["href"] if url_el and url_el.has_attr("href") else None
    description = first([".snippet", ".job-description", ".job-card__description", "p"])
    proposals_text = first([".proposals-count", ".proposal-count", ".jobMeta-data"]) or ""
    proposals = parse_int_from_text(proposals_text)

    budget_text = first([".budget", ".job-budget", ".job-rate"])
    budget_amount = parse_money(budget_text)

    skills = [t.get_text(strip=True) for t in s.select(".tag, .skill, .job-tag")]
    if not skills:
        # try to parse skills from description by splitting on commas for fallback
        if description:
            skills = [x.strip() for x in description.split(",")[:5]]

    client_block = s.select_one(".client, .client-info, .client-block")
    payment_verified = False
    hire_rate = None
    total_spent = None
    location = None
    if client_block:
        if client_block.select_one(".payment-verified, .verified"):
            payment_verified = True
        hr_text = client_block.select_one(".hire-rate, .hire-rate-text")
        if hr_text:
            hire_rate = parse_int_from_text(hr_text.get_text())
        ts = client_block.select_one(".total-spend")
        if ts:
            total_spent = parse_money(ts.get_text())
        loc = client_block.select_one(".location")
        if loc:
            location = loc.get_text(strip=True)

    posted_text = first([".posted", ".time-posted", ".posted-date"])
    posted_date = parse_posted_date(posted_text)

    job_id = url or f"local-{hash(html)}"

    return {
        "job_id": job_id,
        "title": title or "",
        "description": description or "",
        "url": url or "",
        "budget_type": "unknown",
        "budget_amount": budget_amount,
        "proposals_count": proposals,
        "hires_count": 0,
        "interviewing_count": 0,
        "last_viewed": None,
        "client": {
            "payment_verified": bool(payment_verified),
            "hire_rate": hire_rate,
            "total_spent": total_spent,
            "location": location
        },
        "required_skills": skills,
        "posted_date": posted_date,
        "raw": {"html": html}
    }
# parser.py
import re
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from typing import Dict, List, Optional

def parse_int_from_text(text: Optional[str]) -> int:
    if not text:
        return 0
    m = re.search(r"\d+", text.replace(",", ""))
    return int(m.group()) if m else 0

def parse_money(text: Optional[str]) -> float:
    if not text:
        return 0.0
    # simple extract first number, allow commas and decimals
    m = re.search(r"[\d,]+(?:\.\d+)?", text.replace(",", ""))
    return float(m.group()) if m else 0.0

def parse_posted_date(text: Optional[str]) -> Optional[datetime]:
    if not text:
        return None
    text = text.strip().lower()
    # handle "1 hour ago", "2 days ago", "Posted 3 days ago", "Posted today"
    if "hour" in text or "minute" in text:
        return datetime.now(timezone.utc)
    m = re.search(r"(\d+)\s+day", text)
    if m:
        days = int(m.group(1))
        return datetime.now(timezone.utc) - timedelta(days=days)
    # fallback: try parsing ISO-ish
    try:
        return datetime.fromisoformat(text)
    except Exception:
        return None

def job_from_card_html(html: str) -> Dict:
    """
    Convert a single job-card HTML snippet into the canonical job dict.
    Keep selectors flexible: try multiple candidates.
    """
    s = BeautifulSoup(html, "lxml")

    def first(selector_list: List[str]):
        for sel in selector_list:
            el = s.select_one(sel)
            if el:
                return el.get_text(separator=" ", strip=True)
        return None

    title = first(["h4", "h3", ".job-title", ".jobCard-title", "a.job-title"])
    url_el = s.select_one("a")
    url = url_el["href"] if url_el and url_el.has_attr("href") else None
    description = first([".snippet", ".job-description", ".job-card__description", "p"])
    proposals_text = first([".proposals-count", ".proposal-count", ".jobMeta-data"]) or ""
    proposals = parse_int_from_text(proposals_text)

    budget_text = first([".budget", ".job-budget", ".job-rate"])
    budget_amount = parse_money(budget_text)

    skills = [t.get_text(strip=True) for t in s.select(".tag, .skill, .job-tag")]
    if not skills:
        # try to parse skills from description by splitting on commas for fallback
        if description:
            skills = [x.strip() for x in description.split(",")[:5]]

    client_block = s.select_one(".client, .client-info, .client-block")
    payment_verified = False
    hire_rate = None
    total_spent = None
    location = None
    if client_block:
        if client_block.select_one(".payment-verified, .verified"):
            payment_verified = True
        hr_text = client_block.select_one(".hire-rate, .hire-rate-text")
        if hr_text:
            hire_rate = parse_int_from_text(hr_text.get_text())
        ts = client_block.select_one(".total-spend")
        if ts:
            total_spent = parse_money(ts.get_text())
        loc = client_block.select_one(".location")
        if loc:
            location = loc.get_text(strip=True)

    posted_text = first([".posted", ".time-posted", ".posted-date"])
    posted_date = parse_posted_date(posted_text)

    job_id = url or f"local-{hash(html)}"

    return {
        "job_id": job_id,
        "title": title or "",
        "description": description or "",
        "url": url or "",
        "budget_type": "unknown",
        "budget_amount": budget_amount,
        "proposals_count": proposals,
        "hires_count": 0,
        "interviewing_count": 0,
        "last_viewed": None,
        "client": {
            "payment_verified": bool(payment_verified),
            "hire_rate": hire_rate,
            "total_spent": total_spent,
            "location": location
        },
        "required_skills": skills,
        "posted_date": posted_date,
        "raw": {"html": html}
    }
