from fastapi import APIRouter, HTTPException
from backend.models.schemas import PredictionRequest, PredictionResponse
from backend.services.ml_service import get_prediction

router = APIRouter()

@router.post("/", response_model=PredictionResponse)
def predict_outcome(request: PredictionRequest):
    """
    Predict procurement outcome based on features.
    """
    try:
        response = get_prediction(request)
        return response
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error during prediction.")
