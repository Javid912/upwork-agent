# submission.py
async def prepare_copy_and_open(job_url: str, proposal_text: str):
    return {"job_url": job_url, "prefill_text": proposal_text}

# prefill-with-playwright is intentionally interactive and stops before submit
