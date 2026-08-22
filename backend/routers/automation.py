from fastapi import APIRouter, HTTPException, Depends
from backend.models.schemas import AutomationEvaluationRequest, AutomationEvaluationResponse
from backend.services.procurement_automation_service import evaluate_automation

router = APIRouter(prefix="/api/automation", tags=["Automation"])

@router.post("/evaluate", response_model=AutomationEvaluationResponse)
def evaluate_procurement_automation(request: AutomationEvaluationRequest):
    try:
        response = evaluate_automation(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
