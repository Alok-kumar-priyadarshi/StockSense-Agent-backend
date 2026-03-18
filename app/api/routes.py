from fastapi import APIRouter 
from app.schemas.request import AnalyzeRequest
from app.core.orchestrator import run_pipeline

router = APIRouter()

@router.post("/analyze")
async def analyze(request: AnalyzeRequest):
    try:
        return run_pipeline(request.query)
    except Exception as e:
        return {
            "error": "Internal failure",
            "details": str(e)
        }