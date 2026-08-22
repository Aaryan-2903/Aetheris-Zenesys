from pydantic import BaseModel
from typing import Optional, Dict, Any

class NetSuiteStatus(BaseModel):
    status: str
    message: str
    mode: str
    last_sync: Optional[str] = None

class NetSuiteSyncResponse(BaseModel):
    success: bool
    netsuite_id: Optional[str] = None
    error_message: Optional[str] = None
    raw_response: Optional[Dict[str, Any]] = None
