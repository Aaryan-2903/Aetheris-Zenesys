import razorpay
from fastapi import HTTPException
from pydantic_settings import BaseSettings
from backend.models.schemas import PaymentCreateRequest, PaymentCreateResponse, PaymentVerifyRequest
from backend.services.purchase_order_service import get_purchase_order, update_purchase_order

class Settings(BaseSettings):
    RAZORPAY_KEY_ID: str = ""
    RAZORPAY_KEY_SECRET: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()

def get_razorpay_client():
    if not settings.RAZORPAY_KEY_ID or not settings.RAZORPAY_KEY_SECRET:
        raise HTTPException(status_code=500, detail="Razorpay configuration missing")
    return razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def create_payment_order(request: PaymentCreateRequest) -> PaymentCreateResponse:
    client = get_razorpay_client()
    
    po = get_purchase_order(request.purchase_order_id)
    if po.payment_status != "PENDING_PAYMENT":
        raise HTTPException(status_code=400, detail="Purchase order is not pending payment")
        
    amount_in_paise = int(po.total_amount * 100)
    
    order_data = {
        "amount": amount_in_paise,
        "currency": "INR",
        "receipt": po.purchase_order_id
    }
    
    try:
        razorpay_order = client.order.create(data=order_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create Razorpay order: {str(e)}")
        
    # Store the razorpay order ID
    po.razorpay_order_id = razorpay_order["id"]
    update_purchase_order(po)
    
    return PaymentCreateResponse(
        purchase_order_id=po.purchase_order_id,
        razorpay_order_id=razorpay_order["id"],
        amount=amount_in_paise,
        currency="INR",
        key_id=settings.RAZORPAY_KEY_ID,
        payment_status=po.payment_status
    )

def verify_payment(request: PaymentVerifyRequest):
    client = get_razorpay_client()
    
    po = get_purchase_order(request.purchase_order_id)
    if po.payment_status == "PAID":
        raise HTTPException(status_code=400, detail="Payment already processed")
        
    if po.razorpay_order_id != request.razorpay_order_id:
        raise HTTPException(status_code=400, detail="Razorpay order ID mismatch")
        
    try:
        client.utility.verify_payment_signature({
            'razorpay_order_id': request.razorpay_order_id,
            'razorpay_payment_id': request.razorpay_payment_id,
            'razorpay_signature': request.razorpay_signature
        })
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid payment signature")
        
    po.payment_status = "PAID"
    po.razorpay_payment_id = request.razorpay_payment_id
    po.order_tracking_status = "PAYMENT_CONFIRMED"
    update_purchase_order(po)
    
    return {"status": "success", "message": "Payment verified successfully"}
