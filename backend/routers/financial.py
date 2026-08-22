from fastapi import APIRouter
from backend.models.schemas import FinancialExposureRequest, FinancialExposureResponse
from backend.services.financial_service import calculate_financial_exposure

router = APIRouter()

@router.post("/", response_model=FinancialExposureResponse)
def get_financial_exposure(request: FinancialExposureRequest):
    return calculate_financial_exposure(request)
