from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from backend.integrations.netsuite.schemas import NetSuiteStatus, NetSuiteSyncResponse
from backend.integrations.netsuite.adapter import netsuite_adapter

router = APIRouter(prefix="/api/netsuite", tags=["NetSuite Integration"])

class SyncPurchaseOrderRequest(BaseModel):
    purchase_order_id: str
    vendor_id: str
    item_id: str = "DEFAULT_ITEM"
    quantity: int
    unit_price: float

@router.get("/status", response_model=NetSuiteStatus)
def get_netsuite_status():
    """
    Returns the current configuration and connection status of the NetSuite integration.
    """
    try:
        return netsuite_adapter.get_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/sync/purchase-order", response_model=NetSuiteSyncResponse)
def sync_purchase_order(request: SyncPurchaseOrderRequest):
    """
    Synchronizes a Purchase Order to NetSuite manually or via event trigger.
    """
    try:
        response = netsuite_adapter.sync_purchase_order(request.dict())
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
