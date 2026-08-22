from fastapi import HTTPException
from datetime import datetime, timezone
import uuid
from backend.models.schemas import ContractCreateRequest, ContractResponse

# In-memory storage for hackathon prototype
_contracts = {}

def create_contract(request: ContractCreateRequest) -> ContractResponse:
    contract_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    
    contract = ContractResponse(
        contract_id=contract_id,
        procurement_request_id=request.procurement_request_id,
        vendor_id=request.vendor_id,
        buyer_terms=request.buyer_terms,
        vendor_terms=request.vendor_terms,
        payment_terms=request.payment_terms,
        delivery_terms=request.delivery_terms,
        warranty_terms=request.warranty_terms,
        return_replacement_terms=request.return_replacement_terms,
        compliance_requirements=request.compliance_requirements,
        buyer_code_of_conduct=request.buyer_code_of_conduct,
        vendor_code_of_conduct=request.vendor_code_of_conduct,
        status="PENDING_ACCEPTANCE",
        buyer_accepted=False,
        vendor_accepted=False,
        created_at=now,
        accepted_at=None
    )
    
    _contracts[contract_id] = contract
    return contract

def get_contract(contract_id: str) -> ContractResponse:
    if contract_id not in _contracts:
        raise HTTPException(status_code=404, detail="Contract not found")
    return _contracts[contract_id]

def accept_contract(contract_id: str, role: str) -> ContractResponse:
    if contract_id not in _contracts:
        raise HTTPException(status_code=404, detail="Contract not found")
        
    contract = _contracts[contract_id]
    
    if contract.status == "EXPIRED":
        raise HTTPException(status_code=400, detail="Cannot accept an expired contract")
        
    if contract.status == "ACCEPTED":
        raise HTTPException(status_code=400, detail="Contract is already accepted")
        
    if role == "buyer":
        contract.buyer_accepted = True
    elif role == "vendor":
        contract.vendor_accepted = True
    else:
        raise HTTPException(status_code=400, detail="Invalid role")
        
    if contract.buyer_accepted and contract.vendor_accepted:
        contract.status = "ACCEPTED"
        contract.accepted_at = datetime.now(timezone.utc).isoformat()
        
    # Re-assign to trigger Pydantic validation / storage update conceptually
    _contracts[contract_id] = contract
    return contract
