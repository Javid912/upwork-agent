# Quick Fix: Method Not Allowed Error

## Problem
The n8n workflow is using GET method instead of POST for `/fetch/playwright` endpoint, causing "Method Not Allowed" error.

## Immediate Solution

### Option 1: Manual Fix in n8n UI
1. Open your n8n workflow
2. Click on the "Fetch Jobs" HTTP Request node
3. Change **Method** from `GET` to `POST`
4. Make sure **Send Body** is enabled
5. Save and test

### Option 2: Test with Simple Command
First, verify the endpoint works with curl:

```bash
curl -X POST http://localhost:8000/fetch/playwright \
  -H "Content-Type: application/json" \
  -d '{"query": "web scraping", "pages": 1}'
```

### Option 3: Create Simple Test Workflow
Create this minimal workflow in n8n:

**Nodes:**
1. **Manual Trigger** (instead of Cron)
2. **HTTP Request** with these settings:
   - **Method**: POST
   - **URL**: `http://python-service:8000/fetch/playwright`
   - **Headers**: `Content-Type: application/json`
   - **Body**: 
   ```json
   {
     "query": "web scraping csv",
     "pages": 1
   }
   ```

## Root Cause
The workflow JSON shows POST method, but n8n might be defaulting to GET due to:
- Version compatibility issues
- Import/export problems
- Node configuration reset

## Verification Steps
1. **Check FastAPI endpoint**: 
   ```bash
   curl -X POST http://localhost:8000/fetch/playwright -H "Content-Type: application/json" -d '{"query": "test"}'
   ```

2. **Check n8n node settings**:
   - Method: POST
   - Send Body: Enabled
   - Body format: JSON

3. **Test with minimal workflow** before using the complete one

## If Still Not Working
Try this alternative approach:

1. Delete the current "Fetch Jobs" node
2. Add a new HTTP Request node
3. Configure it manually with POST method
4. Test it individually

The endpoint definitely requires POST method as defined in the FastAPI code. The issue is in the n8n node configuration, not the API itself.