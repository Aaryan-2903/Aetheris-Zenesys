from fastapi import APIRouter
from backend.models.schemas import PaymentCreateRequest, PaymentCreateResponse, PaymentVerifyRequest
from backend.services.payment_service import create_payment_order, verify_payment

router = APIRouter()

@router.post("/create-order", response_model=PaymentCreateResponse)
def create_order(request: PaymentCreateRequest):
    return create_payment_order(request)

@router.post("/verify")
def verify(request: PaymentVerifyRequest):
    return verify_payment(request)
