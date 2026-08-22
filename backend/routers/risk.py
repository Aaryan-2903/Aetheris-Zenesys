from fastapi import APIRouter
from backend.models.schemas import RiskAssessmentRequest, RiskAssessmentResponse
from backend.services.risk_service import calculate_risk

router = APIRouter()

@router.post("/", response_model=RiskAssessmentResponse)
def evaluate_risk(request: RiskAssessmentRequest):
    return calculate_risk(request)
