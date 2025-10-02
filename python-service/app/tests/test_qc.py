# tests/test_qc.py
import asyncio
from app.qc import run_qc

import pytest
@pytest.mark.asyncio
async def test_qc_short():
    job = {"required_skills": ["python"]}
    ok, issues = await run_qc(job, "short")
    assert ok is False
    assert "too_short" in issues

