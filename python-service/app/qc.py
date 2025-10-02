# qc.py
from typing import Tuple, List

BANNED_WORDS = ["cheap", "lowest cost", "no guarantee"]

async def run_qc(job, proposal_text) -> Tuple[bool, List[str]]:
    issues = []
    wc = len(proposal_text.split())
    if wc < 140:
        issues.append("too_short")
    if wc > 300:
        issues.append("too_long")
    lower = proposal_text.lower()
    for b in BANNED_WORDS:
        if b in lower:
            issues.append(f"banned_word:{b}")
    if job.get("required_skills"):
        found = any(skill.lower() in lower for skill in job["required_skills"])
        if not found:
            issues.append("missing_required_skills")
    qc_passed = len(issues) == 0
    return qc_passed, issues
