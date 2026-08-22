from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from backend.main import app
from backend.services.purchase_order_service import clear_po_db

client = TestClient(app)

def setup_function():
    clear_po_db()

@patch("backend.services.payment_service.settings")
@patch("backend.services.payment_service.razorpay.Client")
def test_create_payment_order_success(mock_razorpay, mock_settings):
    # Mock settings
    mock_settings.RAZORPAY_KEY_ID = "test_id"
    mock_settings.RAZORPAY_KEY_SECRET = "test_secret"
    
    # Mock razorpay client
    mock_client_instance = MagicMock()
    mock_client_instance.order.create.return_value = {"id": "order_mock123"}
    mock_razorpay.return_value = mock_client_instance

    # Create PO first
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
    po_res = client.post("/api/purchase-orders/", json=po_payload)
    po_id = po_res.json()["purchase_order_id"]

    # Create payment order
    payment_payload = {"purchase_order_id": po_id}
    res = client.post("/api/payments/create-order", json=payment_payload)
    
    assert res.status_code == 200
    data = res.json()
    assert data["purchase_order_id"] == po_id
    assert data["razorpay_order_id"] == "order_mock123"
    assert data["amount"] == 1000000  # 1000.0 * 10 * 100 paise
    assert data["currency"] == "INR"
    assert data["key_id"] == "test_id"
    assert data["payment_status"] == "PENDING_PAYMENT"

@patch("backend.services.payment_service.settings")
def test_create_payment_order_missing_config(mock_settings):
    mock_settings.RAZORPAY_KEY_ID = ""
    mock_settings.RAZORPAY_KEY_SECRET = ""
    
    res = client.post("/api/payments/create-order", json={"purchase_order_id": "PO-XYZ"})
    assert res.status_code == 500
    assert "configuration missing" in res.json()["detail"]

@patch("backend.services.payment_service.settings")
@patch("backend.services.payment_service.razorpay.Client")
def test_verify_payment_success(mock_razorpay, mock_settings):
    mock_settings.RAZORPAY_KEY_ID = "test_id"
    mock_settings.RAZORPAY_KEY_SECRET = "test_secret"
    
    mock_client_instance = MagicMock()
    mock_client_instance.order.create.return_value = {"id": "order_mock123"}
    # verification succeeds if it doesn't throw
    mock_client_instance.utility.verify_payment_signature.return_value = True
    mock_razorpay.return_value = mock_client_instance

    # 1. Create PO
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
    po_id = client.post("/api/purchase-orders/", json=po_payload).json()["purchase_order_id"]

    # 2. Create Payment Order
    client.post("/api/payments/create-order", json={"purchase_order_id": po_id})
    
    # 3. Verify Payment
    verify_payload = {
        "purchase_order_id": po_id,
        "razorpay_order_id": "order_mock123",
        "razorpay_payment_id": "pay_mock123",
        "razorpay_signature": "valid_sig"
    }
    verify_res = client.post("/api/payments/verify", json=verify_payload)
    assert verify_res.status_code == 200
    
    # 4. Check PO status updated
    po_check = client.get(f"/api/purchase-orders/{po_id}").json()
    assert po_check["payment_status"] == "PAID"
    assert po_check["order_tracking_status"] == "PAYMENT_CONFIRMED"
    assert po_check["razorpay_payment_id"] == "pay_mock123"

@patch("backend.services.payment_service.settings")
@patch("backend.services.payment_service.razorpay.Client")
def test_verify_payment_invalid_signature(mock_razorpay, mock_settings):
    mock_settings.RAZORPAY_KEY_ID = "test_id"
    mock_settings.RAZORPAY_KEY_SECRET = "test_secret"
    
    mock_client_instance = MagicMock()
    mock_client_instance.order.create.return_value = {"id": "order_mock123"}
    # Mock signature verification failure
    import razorpay.errors
    mock_client_instance.utility.verify_payment_signature.side_effect = razorpay.errors.SignatureVerificationError("Invalid sig")
    mock_razorpay.return_value = mock_client_instance

    po_id = client.post("/api/purchase-orders/", json={
        "procurement_request_id": "REQ-123", "vendor_id": "VEND-001", "category": "Hardware", 
        "item_description": "Laptops", "quantity": 10, "unit_price": 1000.0,
        "payment_terms": "Net 30", "expected_delivery_date": "2026-09-01"
    }).json()["purchase_order_id"]

    client.post("/api/payments/create-order", json={"purchase_order_id": po_id})
    
    verify_payload = {
        "purchase_order_id": po_id,
        "razorpay_order_id": "order_mock123",
        "razorpay_payment_id": "pay_mock123",
        "razorpay_signature": "invalid_sig"
    }
    verify_res = client.post("/api/payments/verify", json=verify_payload)
    assert verify_res.status_code == 400
    assert "Invalid payment signature" in verify_res.json()["detail"]

@patch("backend.services.payment_service.settings")
@patch("backend.services.payment_service.razorpay.Client")
def test_verify_payment_duplicate_processing(mock_razorpay, mock_settings):
    mock_settings.RAZORPAY_KEY_ID = "test_id"
    mock_settings.RAZORPAY_KEY_SECRET = "test_secret"
    
    mock_client_instance = MagicMock()
    mock_client_instance.order.create.return_value = {"id": "order_mock123"}
    mock_client_instance.utility.verify_payment_signature.return_value = True
    mock_razorpay.return_value = mock_client_instance

    po_id = client.post("/api/purchase-orders/", json={
        "procurement_request_id": "REQ-123", "vendor_id": "VEND-001", "category": "Hardware", 
        "item_description": "Laptops", "quantity": 10, "unit_price": 1000.0,
        "payment_terms": "Net 30", "expected_delivery_date": "2026-09-01"
    }).json()["purchase_order_id"]
    client.post("/api/payments/create-order", json={"purchase_order_id": po_id})
    
    verify_payload = {
        "purchase_order_id": po_id,
        "razorpay_order_id": "order_mock123",
        "razorpay_payment_id": "pay_mock123",
        "razorpay_signature": "valid_sig"
    }
    client.post("/api/payments/verify", json=verify_payload)
    
    # Try again
    verify_res = client.post("/api/payments/verify", json=verify_payload)
    assert verify_res.status_code == 400
    assert "Payment already processed" in verify_res.json()["detail"]

if __name__ == "__main__":
    setup_function()
    test_create_payment_order_missing_config()
    setup_function()
    test_create_payment_order_success()
    setup_function()
    test_verify_payment_success()
    setup_function()
    test_verify_payment_invalid_signature()
    setup_function()
    test_verify_payment_duplicate_processing()
    print("All tests passed!")
