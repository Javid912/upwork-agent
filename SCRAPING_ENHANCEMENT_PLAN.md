# Scraping Enhancement Plan - Production Ready

## Current Status Analysis

### Current Scraping Components:
1. **Playwright Fetcher** ([`playwright_fetcher.py`](upwork-agent/python-service/app/fetcher/playwright_fetcher.py)) - Currently using mock data
2. **RSS Fetcher** ([`rss_fetcher.py`](upwork-agent/python-service/app/fetcher/rss_fetcher.py)) - Basic RSS parsing
3. **Database Schema** - Ready for real job data

### Immediate Issue:
The n8n workflow is using GET method instead of POST for `/fetch/playwright` endpoint.

## Production-Ready Scraping Strategy

### Phase 1: Fix Immediate Issues
1. **Fix HTTP Method** - Ensure n8n uses POST for fetch/playwright
2. **Restore Real Scraping** - Replace mock data with actual Upwork scraping
3. **Update Selectors** - Current selectors are placeholders

### Phase 2: Production Enhancements

#### A. Anti-Bot Protection
- **User Agent Rotation** - Randomize browser fingerprints
- **IP Rotation** - Use proxy services
- **Request Throttling** - Respect rate limits
- **Browser Fingerprinting** - Mimic real user behavior

#### B. Authentication & Session Management
- **Upwork Login** - Handle authentication flows
- **Session Persistence** - Maintain logged-in state
- **Cookie Management** - Handle session cookies
- **2FA Handling** - Support for two-factor authentication

#### C. Data Extraction Quality
- **Comprehensive Job Fields** - Extract all relevant job data
- **Error Recovery** - Handle partial data extraction
- **Data Validation** - Ensure data quality before storage
- **Duplicate Detection** - Avoid processing same jobs multiple times

#### D. Reliability & Monitoring
- **Error Logging** - Detailed error tracking
- **Performance Monitoring** - Track scraping success rates
- **Health Checks** - Monitor scraper health
- **Alerting** - Notify on failures

## Implementation Steps

### Step 1: Fix Current Scraping Code
Update [`playwright_fetcher.py`](upwork-agent/python-service/app/fetcher/playwright_fetcher.py) with:

```python
async def fetch_jobs_with_playwright(query: str, pages: int = 1):
    """
    Production-ready Upwork job scraper
    """
    results = []
    async with async_playwright() as p:
        # Configure browser with anti-detection measures
        browser = await p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        
        # Create context with realistic user agent
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        
        page = await context.new_page()
        
        try:
            for i in range(pages):
                url = f"https://www.upwork.com/search/jobs/?q={query}&page={i+1}"
                
                # Navigate with realistic delays
                await page.goto(url, wait_until="networkidle")
                await page.wait_for_timeout(2000)  # Human-like delay
                
                # Extract job data with proper error handling
                jobs = await extract_job_data(page)
                results.extend(jobs)
                
        except Exception as e:
            print(f"Scraping error: {str(e)}")
        finally:
            await browser.close()
    
    return results
```

### Step 2: Enhanced Data Extraction
Create comprehensive job data extraction:

```python
async def extract_job_data(page):
    """
    Extract detailed job information from Upwork search results
    """
    jobs = []
    
    # Updated selectors for current Upwork HTML structure
    job_cards = await page.query_selector_all('[data-test="job-tile-list"] > div')
    
    for card in job_cards:
        try:
            job_data = {
                "job_id": await extract_job_id(card),
                "title": await extract_title(card),
                "description": await extract_description(card),
                "url": await extract_url(card),
                "budget": await extract_budget(card),
                "proposals_count": await extract_proposals_count(card),
                "client_info": await extract_client_info(card),
                "posted_date": await extract_posted_date(card),
                "skills": await extract_skills(card),
                "engagement": await extract_engagement(card)
            }
            jobs.append(job_data)
        except Exception as e:
            print(f"Error extracting job data: {str(e)}")
            continue
    
    return jobs
```

### Step 3: Add Configuration & Environment Variables
Create configuration for scraping parameters:

```python
# config.py
UPWORK_CONFIG = {
    "base_url": "https://www.upwork.com",
    "search_url": "https://www.upwork.com/search/jobs/",
    "rate_limit_delay": 2,  # seconds between requests
    "max_pages": 5,
    "user_agents": [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        # ... more user agents
    ]
}
```

### Step 4: Implement Error Handling & Retry Logic
```python
async def scrape_with_retry(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await perform_scrape(url)
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
```

## Next Immediate Actions

### 1. Fix n8n HTTP Method
- Change "Fetch Jobs" node from GET to POST
- Test with current mock data first

### 2. Research Current Upwork Structure
- Analyze current Upwork HTML structure
- Update CSS selectors accordingly
- Test selectors manually first

### 3. Implement Real Scraping
- Replace mock data with real scraping
- Start with basic data extraction
- Gradually add more fields

### 4. Add Production Features
- Error handling and logging
- Rate limiting
- Data validation
- Monitoring

## Recommended Approach

Let's implement this step-by-step:

1. **Fix n8n workflow** (POST method)
2. **Research Upwork selectors** (manual testing)
3. **Implement basic scraping** (title, URL, basic info)
4. **Add comprehensive data extraction** (all job fields)
5. **Implement production features** (error handling, monitoring)

This approach ensures we build a robust, production-ready scraping system that can reliably extract Upwork job data.