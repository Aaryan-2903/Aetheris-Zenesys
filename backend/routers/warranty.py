from fastapi import APIRouter
from typing import List
from backend.models.schemas import WarrantyCreateRequest, WarrantyResponse, WarrantyPlan
from backend.services.warranty_service import create_warranty, get_warranty, get_warranty_plans

router = APIRouter()

@router.get("/plans", response_model=List[WarrantyPlan])
def list_warranty_plans():
    return get_warranty_plans()

@router.post("/", response_model=WarrantyResponse, status_code=201)
def add_warranty(request: WarrantyCreateRequest):
    return create_warranty(request)

@router.get("/{warranty_id}", response_model=WarrantyResponse)
def retrieve_warranty(warranty_id: str):
    return get_warranty(warranty_id)
