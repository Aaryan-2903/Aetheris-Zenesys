from fastapi import APIRouter
from backend.models.schemas import BuyerFeedbackRequest, BuyerFeedbackResponse, VendorFeedbackSummary
from backend.services.feedback_service import submit_feedback, get_vendor_feedback_summary

router = APIRouter()

@router.post("/", response_model=BuyerFeedbackResponse)
def create_feedback(request: BuyerFeedbackRequest):
    return submit_feedback(request)

@router.get("/vendor/{vendor_id}", response_model=VendorFeedbackSummary)
def vendor_feedback_summary(vendor_id: str):
    return get_vendor_feedback_summary(vendor_id)
