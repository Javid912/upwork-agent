CREATE TABLE IF NOT EXISTS jobs (
  job_id TEXT PRIMARY KEY,
  title TEXT,
  description TEXT,
  url TEXT,
  budget_type TEXT,
  budget_amount NUMERIC,
  proposals_count INTEGER,
  hires_count INTEGER,
  interviewing_count INTEGER,
  last_viewed TIMESTAMP,
  client_payment_verified BOOLEAN,
  client_hire_rate NUMERIC,
  client_total_spent NUMERIC,
  client_location TEXT,
  required_skills TEXT[],
  posted_date TIMESTAMP,
  raw JSONB,
  fetched_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS scored_jobs (
  job_id TEXT PRIMARY KEY REFERENCES jobs(job_id),
  score INTEGER,
  reasoning TEXT,
  key_requirements TEXT[],
  flags TEXT[],
  recommendation TEXT,
  scored_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS proposals (
  id SERIAL PRIMARY KEY,
  job_id TEXT REFERENCES jobs(job_id),
  proposal_text TEXT,
  generated_at TIMESTAMP DEFAULT now(),
  qc_passed BOOLEAN,
  qc_issues TEXT[],
  status TEXT,
  connects_used INTEGER,
  UNIQUE(job_id, generated_at)
);

CREATE TABLE IF NOT EXISTS application_logs (
  id SERIAL PRIMARY KEY,
  job_id TEXT,
  event_type TEXT,
  message TEXT,
  created_at TIMESTAMP DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_jobs_fetched_at ON jobs (fetched_at);
CREATE INDEX IF NOT EXISTS idx_jobs_posted_date ON jobs (posted_date);
