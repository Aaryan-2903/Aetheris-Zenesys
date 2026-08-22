from fastapi import APIRouter
from backend.models.schemas import RepeatRatioRequest, RepeatRatioResponse
from backend.services.repeat_ratio_service import calculate_repeat_ratio, get_repeat_ratio

router = APIRouter()

@router.post("/", response_model=RepeatRatioResponse)
def compute_repeat_ratio(request: RepeatRatioRequest):
    return calculate_repeat_ratio(request)

@router.get("/{vendor_id}", response_model=RepeatRatioResponse)
def retrieve_repeat_ratio(vendor_id: str):
    return get_repeat_ratio(vendor_id)
