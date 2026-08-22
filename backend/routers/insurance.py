from fastapi import APIRouter
from backend.models.schemas import InsuranceCreateRequest, InsuranceResponse
from backend.services.insurance_service import create_insurance, get_insurance

router = APIRouter()

@router.post("/", response_model=InsuranceResponse, status_code=201)
def add_insurance(request: InsuranceCreateRequest):
    return create_insurance(request)

@router.get("/{insurance_id}", response_model=InsuranceResponse)
def retrieve_insurance(insurance_id: str):
    return get_insurance(insurance_id)
