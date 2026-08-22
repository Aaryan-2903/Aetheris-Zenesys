from fastapi import APIRouter, HTTPException
from backend.models.schemas import ProcurementScoringRequest, ProcurementScoringResponse
from backend.services.scoring_service import calculate_business_score

router = APIRouter()

@router.post("/", response_model=ProcurementScoringResponse)
def score_vendors(request: ProcurementScoringRequest):
    """
    Deterministically scores and ranks vendors based on procurement requirements.
    """
    try:
        response = calculate_business_score(request)
        return response
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error during scoring.")
