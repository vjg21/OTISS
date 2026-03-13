from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from typing import List
import uuid
from datetime import datetime

from app.analyze.unified import analyze_indicator

router = APIRouter()

JOBS = {}

# =========================
# REQUEST MODEL
# =========================
class AsyncBulkRequest(BaseModel):
    indicators: List[str]
    use_otx: bool = False
    use_virustotal: bool = False
    use_urlscan: bool = False
    use_securitytrails: bool = False
    use_dns: bool = False

# =========================
# BACKGROUND JOB
# =========================
def run_bulk_job(job_id: str, req: AsyncBulkRequest):
    results = []
    summary = {
        "malicious": 0,
        "suspicious": 0,
        "benign": 0
    }

    for indicator in req.indicators:
        res = analyze_indicator(
            indicator=indicator,
            use_otx=req.use_otx,
            use_virustotal=req.use_virustotal,
            use_urlscan=req.use_urlscan,
            use_securitytrails=req.use_securitytrails,
            use_dns=req.use_dns
        )

        verdict = res["verdict"].lower()
        summary[verdict] += 1
        results.append(res)

    JOBS[job_id]["status"] = "completed"
    JOBS[job_id]["completed_at"] = datetime.utcnow().isoformat() + "Z"
    JOBS[job_id]["summary"] = summary
    JOBS[job_id]["results"] = results

# =========================
# SUBMIT JOB
# =========================
@router.post("/bulk/async")
def submit_bulk(req: AsyncBulkRequest, bg: BackgroundTasks):
    job_id = str(uuid.uuid4())

    JOBS[job_id] = {
        "job_id": job_id,
        "status": "running",
        "submitted_at": datetime.utcnow().isoformat() + "Z",
        "completed_at": None,
        "total": len(req.indicators),
        "summary": {},
        "results": []
    }

    bg.add_task(run_bulk_job, job_id, req)

    return {
        "job_id": job_id,
        "status": "submitted",
        "total": len(req.indicators)
    }

# =========================
# JOB STATUS
# =========================
@router.get("/bulk/async/{job_id}")
def get_bulk_status(job_id: str):
    job = JOBS.get(job_id)
    if not job:
        return {"error": "Job not found"}

    return job
