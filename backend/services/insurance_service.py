from fastapi import HTTPException
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
import uuid
from backend.models.schemas import InsuranceCreateRequest, InsuranceResponse

_insurance_policies = {}

def get_status_from_dates(start_date: datetime, expiry_date: datetime) -> str:
    now = datetime.now(timezone.utc)
    if now > expiry_date:
        return "EXPIRED"
    if now + relativedelta(days=30) >= expiry_date:
        return "EXPIRING"
    return "ACTIVE"

def create_insurance(request: InsuranceCreateRequest) -> InsuranceResponse:
    try:
        start_date = datetime.fromisoformat(request.start_date)
        expiry_date = datetime.fromisoformat(request.expiry_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use ISO format.")
        
    if expiry_date <= start_date:
        raise HTTPException(status_code=400, detail="Expiry date must be after start date.")
        
    status = get_status_from_dates(start_date, expiry_date)
    
    insurance_id = str(uuid.uuid4())
    insurance = InsuranceResponse(
        insurance_id=insurance_id,
        procurement_request_id=request.procurement_request_id,
        vendor_id=request.vendor_id,
        provider=request.provider,
        policy_number=request.policy_number,
        coverage_amount=request.coverage_amount,
        start_date=start_date.isoformat(),
        expiry_date=expiry_date.isoformat(),
        status=status,
        coverage_description=request.coverage_description
    )
    
    _insurance_policies[insurance_id] = insurance
    return insurance

def get_insurance(insurance_id: str) -> InsuranceResponse:
    if insurance_id not in _insurance_policies:
        raise HTTPException(status_code=404, detail="Insurance not found")
        
    insurance = _insurance_policies[insurance_id]
    start_date = datetime.fromisoformat(insurance.start_date)
    expiry_date = datetime.fromisoformat(insurance.expiry_date)
    insurance.status = get_status_from_dates(start_date, expiry_date)
    
    return insurance
