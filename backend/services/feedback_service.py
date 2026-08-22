import uuid
from datetime import datetime
from backend.models.schemas import BuyerFeedbackRequest, BuyerFeedbackResponse, VendorFeedbackSummary

# In-memory store for MVP
feedback_db = []

def submit_feedback(request: BuyerFeedbackRequest) -> BuyerFeedbackResponse:
    feedback = BuyerFeedbackResponse(
        feedback_id=str(uuid.uuid4()),
        order_id=request.order_id,
        vendor_id=request.vendor_id,
        overall_rating=request.overall_rating,
        quality_rating=request.quality_rating,
        delivery_rating=request.delivery_rating,
        responsiveness_rating=request.responsiveness_rating,
        comments=request.comments,
        created_at=datetime.utcnow().isoformat() + "Z"
    )
    feedback_db.append(feedback)
    return feedback

def get_vendor_feedback_summary(vendor_id: str) -> VendorFeedbackSummary:
    vendor_feedbacks = [f for f in feedback_db if f.vendor_id == vendor_id]
    
    count = len(vendor_feedbacks)
    if count == 0:
        return VendorFeedbackSummary(
            vendor_id=vendor_id,
            feedback_count=0,
            average_overall_rating=0.0,
            average_quality_rating=0.0,
            average_delivery_rating=0.0,
            average_responsiveness_rating=0.0
        )
    
    avg_overall = sum(f.overall_rating for f in vendor_feedbacks) / count
    avg_quality = sum(f.quality_rating for f in vendor_feedbacks) / count
    avg_delivery = sum(f.delivery_rating for f in vendor_feedbacks) / count
    avg_resp = sum(f.responsiveness_rating for f in vendor_feedbacks) / count
    
    return VendorFeedbackSummary(
        vendor_id=vendor_id,
        feedback_count=count,
        average_overall_rating=round(avg_overall, 2),
        average_quality_rating=round(avg_quality, 2),
        average_delivery_rating=round(avg_delivery, 2),
        average_responsiveness_rating=round(avg_resp, 2)
    )

def clear_feedback_db():
    feedback_db.clear()
