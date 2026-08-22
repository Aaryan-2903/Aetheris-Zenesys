from fastapi import APIRouter
from backend.models.schemas import ContractCreateRequest, ContractResponse
from backend.services.contract_service import create_contract, get_contract, accept_contract

router = APIRouter()

@router.post("/", response_model=ContractResponse, status_code=201)
def create_new_contract(request: ContractCreateRequest):
    return create_contract(request)

@router.get("/{contract_id}", response_model=ContractResponse)
def retrieve_contract(contract_id: str):
    return get_contract(contract_id)

@router.post("/{contract_id}/accept/buyer", response_model=ContractResponse)
def buyer_accept(contract_id: str):
    return accept_contract(contract_id, "buyer")

@router.post("/{contract_id}/accept/vendor", response_model=ContractResponse)
def vendor_accept(contract_id: str):
    return accept_contract(contract_id, "vendor")
