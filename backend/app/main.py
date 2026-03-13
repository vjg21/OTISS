from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.analyze.unified import router as unified_router
from app.analyze.bulk import router as bulk_router
from app.vulnerability.routes import router as vuln_router
from app.tools.routes import router as tools_router
from app.stats.routes import router as stats_router

app = FastAPI(
    title="OTISS Threat Intelligence Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(unified_router, prefix="/analyze", tags=["Analyze"])
app.include_router(bulk_router, prefix="/analyze", tags=["Analyze"])
app.include_router(vuln_router, prefix="/vulnerabilities", tags=["Vulnerabilities"])
app.include_router(tools_router, prefix="/tools", tags=["Tools"])
app.include_router(stats_router, prefix="/stats", tags=["Stats"])

@app.get("/")
def root():
    return {"status": "OTISS backend running"}
