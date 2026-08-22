from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from backend.main import app
from backend.services.purchase_order_service import clear_po_db

client = TestClient(app)

def setup_function():
    clear_po_db()

def create_po():
    po_payload = {
        "procurement_request_id": "REQ-123",
        "vendor_id": "VEND-001",
        "category": "Hardware",
        "item_description": "Laptops",
        "quantity": 10,
        "unit_price": 1000.0,
        "payment_terms": "Net 30",
        "expected_delivery_date": "2026-09-01"
    }
    return client.post("/api/purchase-orders/", json=po_payload).json()["purchase_order_id"]

def test_new_po_starts_pending_payment():
    po_id = create_po()
    res = client.get(f"/api/purchase-orders/{po_id}/tracking")
    assert res.status_code == 200
    data = res.json()
    assert data["tracking_status"] == "PENDING_PAYMENT"
    assert len(data["tracking_history"]) == 1
    assert data["tracking_history"][0]["status"] == "PENDING_PAYMENT"
    assert "PAYMENT_CONFIRMED" in data["valid_next_statuses"]

@patch("backend.services.payment_service.settings")
@patch("backend.services.payment_service.razorpay.Client")
def test_successful_payment_changes_tracking(mock_razorpay, mock_settings):
    po_id = create_po()
    
    # Mock settings and razorpay
    mock_settings.RAZORPAY_KEY_ID = "test_id"
    mock_settings.RAZORPAY_KEY_SECRET = "test_secret"
    mock_client = MagicMock()
    mock_client.order.create.return_value = {"id": "order_mock123"}
    mock_client.utility.verify_payment_signature.return_value = True
    mock_razorpay.return_value = mock_client

    client.post("/api/payments/create-order", json={"purchase_order_id": po_id})
    client.post("/api/payments/verify", json={
        "purchase_order_id": po_id,
        "razorpay_order_id": "order_mock123",
        "razorpay_payment_id": "pay_mock123",
        "razorpay_signature": "valid"
    })
    
    # Verify tracking status and history updated
    res = client.get(f"/api/purchase-orders/{po_id}/tracking")
    data = res.json()
    assert data["tracking_status"] == "PAYMENT_CONFIRMED"
    assert len(data["tracking_history"]) == 2
    assert data["tracking_history"][-1]["status"] == "PAYMENT_CONFIRMED"
    assert "PROCESSING" in data["valid_next_statuses"]
    assert "PAYMENT_CONFIRMED" in data["completed_steps"]

def test_valid_transitions():
    po_id = create_po()
    
    # Bypass payment manually via transition (simulate admin or next step)
    client.post(f"/api/purchase-orders/{po_id}/tracking", json={"status": "PAYMENT_CONFIRMED"})
    
    # PROCESSING works
    res = client.post(f"/api/purchase-orders/{po_id}/tracking", json={"status": "PROCESSING"})
    assert res.status_code == 200
    assert res.json()["tracking_status"] == "PROCESSING"

    # SHIPPED works
    res = client.post(f"/api/purchase-orders/{po_id}/tracking", json={"status": "SHIPPED"})
    assert res.status_code == 200
    
    # IN_TRANSIT works
    res = client.post(f"/api/purchase-orders/{po_id}/tracking", json={"status": "IN_TRANSIT"})
    assert res.status_code == 200

    # OUT_FOR_DELIVERY works
    res = client.post(f"/api/purchase-orders/{po_id}/tracking", json={"status": "OUT_FOR_DELIVERY"})
    assert res.status_code == 200

    # DELIVERED works
    res = client.post(f"/api/purchase-orders/{po_id}/tracking", json={"status": "DELIVERED"})
    assert res.status_code == 200
    
    # DELIVERED cannot move back
    res = client.post(f"/api/purchase-orders/{po_id}/tracking", json={"status": "OUT_FOR_DELIVERY"})
    assert res.status_code == 400
    
    tracking_data = client.get(f"/api/purchase-orders/{po_id}/tracking").json()
    assert len(tracking_data["tracking_history"]) == 7

def test_invalid_backward_transitions():
    po_id = create_po()
    client.post(f"/api/purchase-orders/{po_id}/tracking", json={"status": "PAYMENT_CONFIRMED"})
    client.post(f"/api/purchase-orders/{po_id}/tracking", json={"status": "PROCESSING"})
    
    # Cannot move to SHIPPED and back to PROCESSING
    client.post(f"/api/purchase-orders/{po_id}/tracking", json={"status": "SHIPPED"})
    res = client.post(f"/api/purchase-orders/{po_id}/tracking", json={"status": "PROCESSING"})
    assert res.status_code == 400

    # Cannot jump to DELIVERED
    res = client.post(f"/api/purchase-orders/{po_id}/tracking", json={"status": "DELIVERED"})
    assert res.status_code == 400

def test_cancelled_cannot_move_forward():
    po_id = create_po()
    client.post(f"/api/purchase-orders/{po_id}/tracking", json={"status": "PAYMENT_CONFIRMED"})
    client.post(f"/api/purchase-orders/{po_id}/tracking", json={"status": "PROCESSING"})
    
    # Cancel it
    res = client.post(f"/api/purchase-orders/{po_id}/tracking", json={"status": "CANCELLED"})
    assert res.status_code == 200
    
    # Try to ship it
    res = client.post(f"/api/purchase-orders/{po_id}/tracking", json={"status": "SHIPPED"})
    assert res.status_code == 400

def test_invalid_po_handled():
    res = client.get("/api/purchase-orders/INVALID/tracking")
    assert res.status_code == 404

if __name__ == "__main__":
    setup_function()
    test_new_po_starts_pending_payment()
    setup_function()
    test_successful_payment_changes_tracking()
    setup_function()
    test_valid_transitions()
    setup_function()
    test_invalid_backward_transitions()
    setup_function()
    test_cancelled_cannot_move_forward()
    setup_function()
    test_invalid_po_handled()
    print("All tracking tests passed!")
