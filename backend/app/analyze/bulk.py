from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from app.analyze.unified import analyze_indicator

router = APIRouter()

class BulkRequest(BaseModel):
    indicators: List[str]
    use_otx: bool = False
    use_virustotal: bool = False
    use_urlscan: bool = False
    use_securitytrails: bool = False
    use_dns: bool = False

@router.post("/bulk")
def bulk_analyze(req: BulkRequest):
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

    return {
        "count": len(results),
        "summary": summary,
        "results": results
    }
