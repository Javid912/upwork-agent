# Upwork Agent - Implementation Guide

## Quick Start: Get Your n8n Workflow Working

### ✅ What's Already Fixed
1. **Root endpoint added** to FastAPI service
2. **Health check endpoint** available
3. **Complete n8n workflow** created
4. **Database schema** verified working

### 🚀 Immediate Next Steps

## Step 1: Restart Python Service
Since we modified the code, restart the Python service:

```bash
# From your project directory
docker-compose restart python-service
```

## Step 2: Test the Fix
Verify the root endpoint now works:

```bash
# Test the new root endpoint
curl http://localhost:8000/

# Expected response:
# {"message": "Upwork Agent Service", "status": "running"}

# Test health check
curl http://localhost:8000/health

# Expected response:
# {"status": "healthy", "service": "upwork-agent"}
```

## Step 3: Import n8n Workflow
1. Open n8n at http://localhost:5678
2. Go to Workflows → Import from File
3. Select `n8n-workflow-complete.json`
4. Activate the workflow

## Step 4: Test Step-by-Step

### Test 1: Health Check in n8n
- Execute just the "Health Check" node
- Should return: `{"status": "healthy", "service": "upwork-agent"}`

### Test 2: Job Fetching
- Execute up to "Fetch Jobs" node
- Should return job data with inserted IDs

### Test 3: Full Workflow
- Activate the entire workflow
- Let it run automatically every 4 hours

## Step 5: Verify Database Results
Check if jobs are being stored:

```sql
-- Connect to database
docker exec -it postgres_upwork psql -U upwork_user -d upwork_jobs

-- Check jobs table
SELECT job_id, title FROM jobs LIMIT 5;

-- Check scored jobs
SELECT * FROM scored_jobs LIMIT 5;

-- Check proposals
SELECT * FROM proposals LIMIT 5;
```

## 🎯 Workflow Logic Explained

### Job Processing Flow:
1. **Cron Trigger** → Runs every 4 hours
2. **Health Check** → Verifies service availability
3. **Fetch Jobs** → Scrapes Upwork for "web scraping csv" jobs
4. **Analyze Jobs** → Scores each job (1-10 scale)
5. **Score Check** → Only processes jobs with score > 7
6. **Generate Proposal** → Creates AI-powered proposal
7. **QC Check** → Validates proposal quality
8. **Prepare Submission** → Finalizes for human review

### Error Handling:
- **Low scoring jobs** → Logged and skipped
- **QC failed proposals** → Logged and skipped
- **Service unavailable** → Workflow stops gracefully

## 🔧 Customization Options

### Change Search Query:
Edit the "Set Search Query" node:
```javascript
// Current: "web scraping csv"
const searchQuery = "your search terms here";
```

### Adjust Scoring Threshold:
Edit the "Score Check" node:
- Change `$json.score > 7` to your preferred threshold

### Add Notifications:
Add these nodes after "Log Success":
- **Email node** for approval requests
- **Slack node** for team notifications
- **Webhook node** for external systems

## 🐛 Troubleshooting Common Issues

### Issue: "Service not found" in n8n
- **Solution**: Use `http://python-service:8000` (not localhost)
- **Verify**: Check if Python service is running: `docker ps`

### Issue: No jobs found
- **Cause**: Playwright selectors need updating for real Upwork HTML
- **Solution**: Update selectors in `playwright_fetcher.py`

### Issue: Database connection errors
- **Verify**: Check if PostgreSQL is running: `docker ps`
- **Test**: `docker exec -it postgres_upwork psql -U upwork_user -d upwork_jobs -c "SELECT 1;"`

### Issue: Proposal generation fails
- **Note**: LLM integration is currently stubbed
- **Solution**: Replace dummy implementation in `generator.py` with real API calls

## 📈 Monitoring & Logs

### Check n8n Execution:
- Go to n8n UI → Executions
- View detailed logs for each run
- See which nodes succeeded/failed

### Database Monitoring:
```sql
-- Monitor job processing
SELECT COUNT(*) as total_jobs FROM jobs;
SELECT COUNT(*) as scored_jobs FROM scored_jobs;
SELECT COUNT(*) as proposals FROM proposals;

-- Check recent activity
SELECT * FROM application_logs ORDER BY created_at DESC LIMIT 10;
```

## 🎉 Success Indicators

Your system is working when:
- ✅ n8n workflow runs without errors
- ✅ Jobs appear in the database
- ✅ Jobs get scored automatically
- ✅ Proposals are generated for high-scoring jobs
- ✅ Human approval requests are created

## Next Enhancement Steps
1. **Real Upwork Integration**: Update Playwright selectors
2. **LLM Integration**: Connect to DeepSeek/OpenAI API
3. **Email Notifications**: Add approval workflow
4. **Advanced Scoring**: Improve job evaluation logic
5. **Multiple Job Sources**: Add RSS feeds and other platforms

## Ready to Go!
Your Upwork Agent is now ready for testing. Start with the health check and gradually test each component. The system will automatically discover, score, and prepare job applications for your review every 4 hours.