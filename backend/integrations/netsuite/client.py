import os
import uuid
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class LiveNetSuiteClient:
    """
    Client for live NetSuite ERP connections using OAuth 2.0 or TBA.
    Fails safely if credentials are not present.
    """
    def __init__(self):
        self.account_id = os.getenv("NETSUITE_ACCOUNT_ID")
        self.client_id = os.getenv("NETSUITE_CLIENT_ID")
        self.client_secret = os.getenv("NETSUITE_CLIENT_SECRET")
        self.base_url = os.getenv("NETSUITE_BASE_URL")
        
        self.is_configured = bool(self.account_id and self.client_id and self.client_secret)

    def is_available(self) -> bool:
        return self.is_configured

    def send_record(self, record_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.is_available():
            raise Exception("NetSuite connection not configured")
        # In a real scenario, make a REST API call here.
        # This is a stub for when credentials become available.
        raise NotImplementedError("Live NetSuite Sync not yet implemented.")


class MockNetSuiteClient:
    """
    Mock client for local development and demonstration.
    Pretends to interact with NetSuite successfully.
    """
    def is_available(self) -> bool:
        return True

    def send_record(self, record_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"MockNetSuiteClient: Syncing {record_type} to NetSuite (Mock). Data: {data}")
        # Return a fake NetSuite Internal ID
        return {
            "internal_id": f"ns_{uuid.uuid4().hex[:8]}",
            "status": "success",
            "record_type": record_type
        }
