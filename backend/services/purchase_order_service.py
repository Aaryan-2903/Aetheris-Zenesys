import uuid
import io
from datetime import datetime
from backend.models.schemas import PurchaseOrderRequest, PurchaseOrderResponse, TrackingHistoryEvent, OrderTrackingResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from fastapi import HTTPException

# In-memory store for MVP
purchase_order_db = []

VALID_TRANSITIONS = {
    "PENDING_PAYMENT": ["PAYMENT_CONFIRMED", "CANCELLED"],
    "PAYMENT_CONFIRMED": ["PROCESSING"],
    "PROCESSING": ["SHIPPED", "CANCELLED"],
    "SHIPPED": ["IN_TRANSIT"],
    "IN_TRANSIT": ["OUT_FOR_DELIVERY"],
    "OUT_FOR_DELIVERY": ["DELIVERED"],
    "DELIVERED": [],
    "CANCELLED": []
}

ALL_STEPS = [
    "PENDING_PAYMENT", 
    "PAYMENT_CONFIRMED", 
    "PROCESSING", 
    "SHIPPED", 
    "IN_TRANSIT", 
    "OUT_FOR_DELIVERY", 
    "DELIVERED"
]

def create_purchase_order(request: PurchaseOrderRequest) -> PurchaseOrderResponse:
    subtotal = request.quantity * request.unit_price
    total_amount = subtotal + request.warranty_fee + request.insurance_cost
    now_iso = datetime.utcnow().isoformat() + "Z"
    
    initial_event = TrackingHistoryEvent(status="PENDING_PAYMENT", timestamp=now_iso)
    
    po = PurchaseOrderResponse(
        purchase_order_id=f"PO-{str(uuid.uuid4())[:8].upper()}",
        procurement_request_id=request.procurement_request_id,
        vendor_id=request.vendor_id,
        vendor_name=f"Vendor {request.vendor_id}", # mock name
        category=request.category,
        item_description=request.item_description,
        quantity=request.quantity,
        unit_price=request.unit_price,
        subtotal=subtotal,
        selected_warranty_plan=request.selected_warranty_plan,
        warranty_fee=request.warranty_fee,
        insurance_provider=request.insurance_provider,
        insurance_cost=request.insurance_cost,
        total_amount=total_amount,
        payment_terms=request.payment_terms,
        expected_delivery_date=request.expected_delivery_date,
        contract_id=request.contract_id,
        warranty_id=request.warranty_id,
        insurance_id=request.insurance_id,
        return_and_refund_policy=request.return_and_refund_policy,
        payment_status="PENDING_PAYMENT",
        status="Created",
        order_tracking_status="PENDING_PAYMENT",
        tracking_updated_at=now_iso,
        tracking_history=[initial_event],
        razorpay_order_id=None,
        razorpay_payment_id=None,
        created_at=now_iso
    )
    purchase_order_db.append(po)
    return po

def get_purchase_order(purchase_order_id: str) -> PurchaseOrderResponse:
    for po in purchase_order_db:
        if po.purchase_order_id == purchase_order_id:
            return po
    raise HTTPException(status_code=404, detail="Purchase Order not found")

def update_purchase_order(po: PurchaseOrderResponse):
    for i, existing_po in enumerate(purchase_order_db):
        if existing_po.purchase_order_id == po.purchase_order_id:
            purchase_order_db[i] = po
            return po
    raise HTTPException(status_code=404, detail="Purchase Order not found")

def get_tracking_info(po: PurchaseOrderResponse) -> OrderTrackingResponse:
    current_status = po.order_tracking_status
    valid_next = VALID_TRANSITIONS.get(current_status, [])
    
    # Calculate completed steps
    completed_steps = []
    next_step = None
    if current_status == "CANCELLED":
        completed_steps = [e.status for e in po.tracking_history]
    else:
        try:
            curr_idx = ALL_STEPS.index(current_status)
            completed_steps = ALL_STEPS[:curr_idx + 1]
            if curr_idx + 1 < len(ALL_STEPS):
                next_step = ALL_STEPS[curr_idx + 1]
        except ValueError:
            pass

    return OrderTrackingResponse(
        purchase_order_id=po.purchase_order_id,
        tracking_status=current_status,
        expected_delivery_date=po.expected_delivery_date,
        tracking_updated_at=po.tracking_updated_at,
        tracking_history=po.tracking_history,
        valid_next_statuses=valid_next,
        current_status=current_status,
        completed_steps=completed_steps,
        next_step=next_step
    )

def transition_tracking_status(purchase_order_id: str, new_status: str) -> OrderTrackingResponse:
    po = get_purchase_order(purchase_order_id)
    current_status = po.order_tracking_status
    
    if new_status not in VALID_TRANSITIONS.get(current_status, []):
        raise HTTPException(status_code=400, detail=f"Invalid transition from {current_status} to {new_status}")
    
    now_iso = datetime.utcnow().isoformat() + "Z"
    po.order_tracking_status = new_status
    po.tracking_updated_at = now_iso
    po.tracking_history.append(TrackingHistoryEvent(status=new_status, timestamp=now_iso))
    
    update_purchase_order(po)
    return get_tracking_info(po)


def generate_purchase_order_pdf(purchase_order_id: str) -> io.BytesIO:
    po = get_purchase_order(purchase_order_id)
    
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, height - 50, "ProcuraIQ")
    c.setFont("Helvetica", 14)
    c.drawString(50, height - 70, "Purchase Order / Invoice-style Prototype")
    
    # PO Info
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 110, f"Purchase Order ID: {po.purchase_order_id}")
    c.drawString(50, height - 130, f"Date: {po.created_at[:10]}")
    c.drawString(50, height - 150, f"Vendor: {po.vendor_name} ({po.vendor_id})")
    c.drawString(50, height - 170, f"Procurement Request ID: {po.procurement_request_id}")
    c.drawString(50, height - 190, f"Category: {po.category}")
    
    # Line Items
    y = height - 240
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Item Description")
    c.drawString(300, y, "Qty")
    c.drawString(400, y, "Unit Price")
    c.drawString(500, y, "Total")
    
    c.line(50, y - 5, 550, y - 5)
    
    y -= 20
    c.setFont("Helvetica", 12)
    c.drawString(50, y, str(po.item_description))
    c.drawString(300, y, str(po.quantity))
    c.drawString(400, y, f"${po.unit_price:.2f}")
    c.drawString(500, y, f"${po.subtotal:.2f}")
    
    # Optional Items
    if po.selected_warranty_plan:
        y -= 20
        c.drawString(50, y, f"Warranty: {po.selected_warranty_plan}")
        c.drawString(300, y, "1")
        c.drawString(400, y, f"${po.warranty_fee:.2f}")
        c.drawString(500, y, f"${po.warranty_fee:.2f}")
        
    if po.insurance_provider:
        y -= 20
        c.drawString(50, y, f"Insurance: {po.insurance_provider}")
        c.drawString(300, y, "1")
        c.drawString(400, y, f"${po.insurance_cost:.2f}")
        c.drawString(500, y, f"${po.insurance_cost:.2f}")
        
    c.line(50, y - 10, 550, y - 10)
    
    # Total
    y -= 30
    c.setFont("Helvetica-Bold", 14)
    c.drawString(400, y, "TOTAL AMOUNT:")
    c.drawString(500, y, f"${po.total_amount:.2f}")
    
    # Terms and details
    y -= 50
    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Payment Terms: {po.payment_terms}")
    c.drawString(50, y - 15, f"Expected Delivery Date: {po.expected_delivery_date}")
    
    y -= 45
    if po.contract_id:
        c.drawString(50, y, f"Contract ID: {po.contract_id}")
        y -= 15
    if po.warranty_id:
        c.drawString(50, y, f"Warranty ID: {po.warranty_id}")
        y -= 15
    if po.insurance_id:
        c.drawString(50, y, f"Insurance ID: {po.insurance_id}")
        y -= 15
        
    y -= 15
    c.drawString(50, y, f"Payment Status: {po.payment_status}")
    c.drawString(50, y - 15, f"Purchase Order Status: {po.status}")
    
    if po.return_and_refund_policy:
        y -= 30
        c.setFont("Helvetica-Bold", 11)
        c.drawString(50, y, "Return & Refund Policy")
        y -= 15
        c.setFont("Helvetica", 9)
        c.drawString(50, y, f"Return Window: {po.return_and_refund_policy.return_window_days} days | Refund Processing: {po.return_and_refund_policy.refund_processing_days} days")
        y -= 15
        c.drawString(50, y, f"Eligible Conditions: {po.return_and_refund_policy.eligible_return_conditions}")
        y -= 15
        c.drawString(50, y, f"Refund Method: {po.return_and_refund_policy.refund_method}")
        y -= 15
        c.drawString(50, y, f"Return Shipping Responsibility: {po.return_and_refund_policy.return_shipping_responsibility}")
        y -= 15
        c.drawString(50, y, f"Restocking Fee: {po.return_and_refund_policy.restocking_fee_percentage}%")
        y -= 15
        c.drawString(50, y, f"Non-returnable Conditions: {po.return_and_refund_policy.non_returnable_conditions}")

    # Footer
    c.setFont("Helvetica-Oblique", 10)
    c.drawCentredString(width / 2.0, 30, "Generated by ProcuraIQ — AI-Assisted Procurement Decision Intelligence Platform")
    
    c.save()
    buffer.seek(0)
    return buffer

def clear_po_db():
    purchase_order_db.clear()
