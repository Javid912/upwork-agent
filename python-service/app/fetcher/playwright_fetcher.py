# playwright_fetcher.py
from playwright.async_api import async_playwright
import asyncio, time

async def scrape_search_page(page, url):
    await page.goto(url, wait_until="networkidle")
    # NOTE: selectors below are placeholders — update according to target website
    cards = await page.query_selector_all("section.job-tile")
    jobs = []
    for c in cards:
        title_el = await c.query_selector("h4")
        title = (await title_el.inner_text()) if title_el else ""
        url_el = await c.query_selector("a")
        job_url = await url_el.get_attribute("href") if url_el else ""
        jobs.append({
            "job_id": job_url or f"local-{int(time.time()*1000)}",
            "title": title.strip(),
            "description": "",
            "url": job_url,
            "proposals_count": 0, "hires_count": 0, "interviewing_count": 0,
            "client": {"payment_verified": None, "hire_rate": None, "total_spent": None, "location": None},
            "required_skills": [],
            "posted_date": None,
            "raw": {}
        })
    return jobs

async def fetch_jobs_with_playwright(query: str, pages:int=1):
    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        for i in range(pages):
            url = f"https://www.upwork.com/search/jobs/?q={query}&page={i+1}"
            jobs = await scrape_search_page(page, url)
            results.extend(jobs)
        await browser.close()
    return results

# wrapper for non-async contexts if needed
def fetch_jobs_with_playwright_sync(query: str, pages: int = 1):
    return asyncio.get_event_loop().run_until_complete(fetch_jobs_with_playwright(query, pages))
