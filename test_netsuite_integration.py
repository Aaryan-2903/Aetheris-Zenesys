import os
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_netsuite_status_mock_mode():
    # NETSUITE_USE_MOCK is set to true via .env.example hypothetically,
    # but let's test the endpoint as it is currently configured.
    # We can inject os.environ for testing if needed, but the current adapter
    # already loaded it. Let's just check the endpoint returns a valid status.
    response = client.get("/api/netsuite/status")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "mode" in data
    
    # It should be either DEVELOPMENT/MOCK or CONFIGURATION REQUIRED
    # since we don't have live credentials.
    assert data["mode"] in ["DEVELOPMENT/MOCK", "CONFIGURATION REQUIRED"]

def test_netsuite_sync_purchase_order():
    # If in mock mode, this should succeed. If in required config mode, it should return success=False.
    response = client.post("/api/netsuite/sync/purchase-order", json={
        "purchase_order_id": "PO-TEST",
        "vendor_id": "V-1234",
        "item_id": "ITEM-1",
        "quantity": 10,
        "unit_price": 50.0
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    
    # Verify we don't crash
    if data["success"]:
        assert "netsuite_id" in data
    else:
        assert "error_message" in data
        assert "NetSuite connection not configured" in data["error_message"]

if __name__ == "__main__":
    test_netsuite_status_mock_mode()
    test_netsuite_sync_purchase_order()
    print("All NetSuite integration tests passed!")
