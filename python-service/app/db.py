# db.py
import os, asyncpg
from typing import Optional

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://upwork_agent:changeme@postgres:5432/upwork_agent_db")

class Database:
    def __init__(self):
        self.pool: Optional[asyncpg.pool.Pool] = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=10)

    async def disconnect(self):
        if self.pool:
            await self.pool.close()

    async def upsert_job(self, job: dict) -> bool:
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO jobs (job_id, title, description, url, budget_type, budget_amount, proposals_count,
                                  hires_count, interviewing_count, last_viewed, client_payment_verified, client_hire_rate,
                                  client_total_spent, client_location, required_skills, posted_date, raw)
                VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17)
                ON CONFLICT (job_id) DO UPDATE
                SET (title, description, url, budget_type, budget_amount, proposals_count, hires_count,
                     interviewing_count, last_viewed, client_payment_verified, client_hire_rate, client_total_spent,
                     client_location, required_skills, posted_date, raw, fetched_at) =
                    (EXCLUDED.title, EXCLUDED.description, EXCLUDED.url, EXCLUDED.budget_type, EXCLUDED.budget_amount,
                     EXCLUDED.proposals_count, EXCLUDED.hires_count, EXCLUDED.interviewing_count, EXCLUDED.last_viewed,
                     EXCLUDED.client_payment_verified, EXCLUDED.client_hire_rate, EXCLUDED.client_total_spent,
                     EXCLUDED.client_location, EXCLUDED.required_skills, EXCLUDED.posted_date, EXCLUDED.raw, now())
                """,
                job["job_id"], job.get("title"), job.get("description"), job.get("url"),
                job.get("budget_type"), job.get("budget_amount"), job.get("proposals_count"),
                job.get("hires_count"), job.get("interviewing_count"), job.get("last_viewed"),
                job.get("client", {}).get("payment_verified"),
                job.get("client", {}).get("hire_rate"),
                job.get("client", {}).get("total_spent"),
                job.get("client", {}).get("location"),
                job.get("required_skills"),
                job.get("posted_date"),
                str(job)  # Convert dict to string for raw field
            )
        return True

    async def get_job(self, job_id: str) -> dict:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM jobs WHERE job_id=$1", job_id)
            return dict(row) if row else None

    async def upsert_scored_job(self, job_id, score, reasoning, key_requirements, flags, recommendation=None):
        async with self.pool.acquire() as conn:
            await conn.execute("""
            INSERT INTO scored_jobs (job_id, score, reasoning, key_requirements, flags, recommendation)
            VALUES ($1,$2,$3,$4,$5,$6)
            ON CONFLICT (job_id) DO UPDATE SET score=EXCLUDED.score, reasoning=EXCLUDED.reasoning, key_requirements=EXCLUDED.key_requirements, flags=EXCLUDED.flags, recommendation=EXCLUDED.recommendation, scored_at=now()
            """, job_id, score, reasoning, key_requirements, flags, recommendation or '')

    async def insert_proposal(self, job_id, proposal_text, qc_passed, qc_issues, status="pending"):
        async with self.pool.acquire() as conn:
            await conn.execute("""
            INSERT INTO proposals (job_id, proposal_text, qc_passed, qc_issues, status)
            VALUES ($1,$2,$3,$4,$5)
            """, job_id, proposal_text, qc_passed, qc_issues, status)

    async def get_latest_proposal(self, job_id):
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM proposals WHERE job_id=$1 ORDER BY generated_at DESC LIMIT 1", job_id)
            return dict(row) if row else None
