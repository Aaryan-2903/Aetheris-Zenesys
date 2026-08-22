from fastapi import HTTPException
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
import uuid
from backend.models.schemas import WarrantyCreateRequest, WarrantyResponse, WarrantyPlan

_warranties = {}

PREDEFINED_PLANS = {
    "plan_std": WarrantyPlan(plan_id="plan_std", plan_name="Standard", warranty_period_months=12, warranty_fee=0.0, coverage_description="Standard basic coverage"),
    "plan_ext": WarrantyPlan(plan_id="plan_ext", plan_name="Extended", warranty_period_months=24, warranty_fee=150.0, coverage_description="Extended parts and labor"),
    "plan_prem": WarrantyPlan(plan_id="plan_prem", plan_name="Premium", warranty_period_months=36, warranty_fee=300.0, coverage_description="Premium next-day replacement")
}

def get_warranty_plans() -> list[WarrantyPlan]:
    return list(PREDEFINED_PLANS.values())

def get_status_from_dates(start_date: datetime, expiry_date: datetime) -> str:
    now = datetime.now(timezone.utc)
    if now > expiry_date:
        return "EXPIRED"
    if now + relativedelta(days=30) >= expiry_date:
        return "EXPIRING"
    return "ACTIVE"

def create_warranty(request: WarrantyCreateRequest) -> WarrantyResponse:
    if request.plan_id not in PREDEFINED_PLANS:
        raise HTTPException(status_code=400, detail="Invalid plan ID")
        
    plan = PREDEFINED_PLANS[request.plan_id]
    warranty_id = str(uuid.uuid4())
    
    try:
        start_date = datetime.fromisoformat(request.warranty_start_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid start date format. Use ISO format.")
        
    expiry_date = start_date + relativedelta(months=plan.warranty_period_months)
    status = get_status_from_dates(start_date, expiry_date)
    
    warranty = WarrantyResponse(
        warranty_id=warranty_id,
        procurement_request_id=request.procurement_request_id,
        vendor_id=request.vendor_id,
        product_or_service=request.product_or_service,
        plan_id=plan.plan_id,
        warranty_period_months=plan.warranty_period_months,
        warranty_fee=plan.warranty_fee,
        warranty_start_date=start_date.isoformat(),
        warranty_expiry_date=expiry_date.isoformat(),
        status=status,
        coverage_description=plan.coverage_description,
        claim_reference=None
    )
    
    _warranties[warranty_id] = warranty
    return warranty

def get_warranty(warranty_id: str) -> WarrantyResponse:
    if warranty_id not in _warranties:
        raise HTTPException(status_code=404, detail="Warranty not found")
        
    warranty = _warranties[warranty_id]
    if warranty.status != "CLAIMED":
        start_date = datetime.fromisoformat(warranty.warranty_start_date)
        expiry_date = datetime.fromisoformat(warranty.warranty_expiry_date)
        warranty.status = get_status_from_dates(start_date, expiry_date)
        
    return warranty
