# playwright_fetcher.py
import asyncio
import random
from typing import List, Optional
from playwright.async_api import async_playwright
from .parser import job_from_card_html
import time

async def fetch_search_page_content(page, url: str):
    await page.goto(url, wait_until="networkidle")
    # small sleep to allow dynamic rendering
    await asyncio.sleep(random.uniform(0.5, 1.2))
    return await page.content()

def extract_job_card_htmls_from_page(html: str) -> List[str]:
    # Use BeautifulSoup in parser if needed, but for speed we can use CSS split patterns.
    # Here we just reuse the parser approach: find elements that look like job cards.
    from bs4 import BeautifulSoup
    s = BeautifulSoup(html, "lxml")
    # Try multiple likely selectors:
    candidates = [
        "section.job-tile", "article.job-tile", ".up-card-section", ".job-card",
        ".job-tile", "div.job"
    ]
    cards = []
    for sel in candidates:
        elts = s.select(sel)
        if elts:
            cards = elts
            break
    if not cards:
        # fallback: try to guess elements that have job-title inside
        cards = s.select("a:has(h4), a:has(h3)")
    return [str(card) for card in cards]

async def fetch_jobs_with_playwright(query: str, pages: int = 1, storage_state: Optional[str] = None, headless: bool = True) -> List[dict]:
    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        context_kwargs = {}
        if storage_state:
            context_kwargs["storage_state"] = storage_state
        context = await browser.new_context(**context_kwargs)
        page = await context.new_page()

        # build search url — you will replace with the exact Upwork search URL encoding
        for page_no in range(1, pages + 1):
            url = f"https://www.upwork.com/search/jobs/?q={query.replace(' ', '+')}&page={page_no}"
            try:
                html = await fetch_search_page_content(page, url)
            except Exception as e:
                print("page fetch failed:", e)
                continue
            card_htmls = extract_job_card_htmls_from_page(html)
            for card_html in card_htmls:
                job = job_from_card_html(card_html)
                results.append(job)
            # polite pause
            await asyncio.sleep(random.uniform(1.0, 2.5))
        await browser.close()
    return results

# sync wrapper for local convenience
def fetch_jobs_sync(query: str, pages: int = 1, storage_state: Optional[str] = None, headless: bool = True):
    return asyncio.get_event_loop().run_until_complete(fetch_jobs_with_playwright(query, pages, storage_state, headless))
