from fastapi import APIRouter, Response
from backend.models.schemas import PurchaseOrderRequest, PurchaseOrderResponse, OrderTrackingResponse, OrderTrackingUpdateRequest
from backend.services.purchase_order_service import create_purchase_order, get_purchase_order, generate_purchase_order_pdf, get_tracking_info, transition_tracking_status

router = APIRouter()

@router.post("/", response_model=PurchaseOrderResponse)
def create_po(request: PurchaseOrderRequest):
    return create_purchase_order(request)

@router.get("/{purchase_order_id}", response_model=PurchaseOrderResponse)
def get_po(purchase_order_id: str):
    return get_purchase_order(purchase_order_id)

@router.get("/{purchase_order_id}/tracking", response_model=OrderTrackingResponse)
def get_po_tracking(purchase_order_id: str):
    po = get_purchase_order(purchase_order_id)
    return get_tracking_info(po)

@router.post("/{purchase_order_id}/tracking", response_model=OrderTrackingResponse)
def update_po_tracking(purchase_order_id: str, request: OrderTrackingUpdateRequest):
    return transition_tracking_status(purchase_order_id, request.status)

@router.get("/{purchase_order_id}/pdf")
def get_po_pdf(purchase_order_id: str):
    pdf_buffer = generate_purchase_order_pdf(purchase_order_id)
    return Response(content=pdf_buffer.getvalue(), media_type="application/pdf")
