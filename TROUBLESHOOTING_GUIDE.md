# Upwork Agent - Troubleshooting & Implementation Guide

## Current Issue: n8n Cannot Connect to Python Service

### Problem Analysis
- **Root Cause**: FastAPI service doesn't have a root endpoint (`/`)
- **Current URL**: `http://python-service:8000/` returns 404
- **Working URLs**: All API endpoints exist but need specific paths

### Step-by-Step Solution

## 1. Test FastAPI Endpoints Directly

First, verify the Python service is working by testing endpoints directly:

```bash
# Test root endpoint (currently fails)
curl http://localhost:8000/

# Test actual endpoints (should work)
curl -X POST http://localhost:8000/fetch/playwright \
  -H "Content-Type: application/json" \
  -d '{"query": "web scraping", "pages": 1}'

# Test health check
curl http://localhost:8000/docs
```

## 2. Fix FastAPI Service (Code Changes Needed)

Switch to Code mode to make these changes to `python-service/app/main.py`:

```python
# Add this endpoint to main.py
@app.get("/")
async def root():
    return {"message": "Upwork Agent Service", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "upwork-agent"}
```

## 3. Updated n8n Workflow Configuration

Replace the current HTTP Request node with these working endpoints:

### Option A: Test Connection (Use this first)
- **URL**: `http://python-service:8000/health`
- **Method**: GET
- **Authentication**: None

### Option B: Fetch Jobs (Working endpoint)
- **URL**: `http://python-service:8000/fetch/playwright`
- **Method**: POST
- **Headers**: `Content-Type: application/json`
- **Body**: 
```json
{
  "query": "web scraping csv",
  "pages": 1
}
```

## 4. Complete n8n Workflow Structure

Create this workflow in n8n for full automation:

### Workflow Nodes:
1. **Cron Trigger** (every 4 hours)
2. **HTTP Request** → Fetch Jobs
3. **Code Node** → Process job IDs
4. **For Each** → Loop through jobs
5. **HTTP Request** → Analyze/Score Job
6. **HTTP Request** → Generate Proposal
7. **If Node** → QC Check
8. **HTTP Request** → Prepare Submission
9. **Email/Slack** → Human Approval

### Example HTTP Request Configuration:
```json
{
  "method": "POST",
  "url": "http://python-service:8000/fetch/playwright",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "query": "{{ $node[\"Cron\"].json.query }}",
    "pages": 1
  }
}
```

## 5. Testing Sequence

Follow this testing order:

1. **Test Service Connectivity**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Test Job Fetching**
   ```bash
   curl -X POST http://localhost:8000/fetch/playwright \
     -H "Content-Type: application/json" \
     -d '{"query": "test", "pages": 1}'
   ```

3. **Check Database**
   ```sql
   SELECT * FROM jobs LIMIT 5;
   ```

4. **Test n8n Workflow**
   - Start with simple HTTP request to `/health`
   - Then test job fetching
   - Gradually add more nodes

## 6. Common Issues & Solutions

### Issue: "Service not found"
- **Cause**: Docker DNS resolution problem
- **Fix**: Use `http://python-service:8000` (not localhost) from n8n

### Issue: 404 Errors
- **Cause**: Wrong endpoint path
- **Fix**: Use exact endpoints from FastAPI docs

### Issue: Database Connection
- **Cause**: Schema not initialized
- **Status**: ✅ Verified working

### Issue: Playwright Scraping
- **Note**: Current selectors are placeholders - update for real Upwork HTML

## 7. Next Steps

1. **Immediate**: Test `/fetch/playwright` endpoint directly
2. **Quick Fix**: Add root endpoint to FastAPI
3. **Workflow**: Build comprehensive n8n workflow
4. **Enhancement**: Update Playwright selectors for real Upwork

## 8. API Endpoints Reference

| Endpoint | Method | Purpose | Parameters |
|----------|--------|---------|------------|
| `/` | GET | Service status | None |
| `/health` | GET | Health check | None |
| `/fetch/rss` | POST | Fetch RSS jobs | `feed_url` |
| `/fetch/playwright` | POST | Scrape jobs | `query`, `pages` |
| `/analyze/{job_id}` | POST | Score job | `job_id` |
| `/generate/{job_id}` | POST | Generate proposal | `job_id` |
| `/prepare_submission/{job_id}` | POST | Prepare submission | `job_id` |

## 9. n8n Tips for Beginners

- **Start Simple**: Test one node at a time
- **Use Debug Mode**: Click "Execute Node" to test individually
- **Check Logs**: View execution details in n8n UI
- **Environment Variables**: Store API keys in n8n settings
- **Error Handling**: Add error branches to workflows

## Ready to Proceed?

Your system is 90% ready! The main issue is the missing root endpoint. Once you add that, your n8n workflow will connect successfully.