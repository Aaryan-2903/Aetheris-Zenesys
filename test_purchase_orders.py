from fastapi.testclient import TestClient
from backend.main import app
from backend.services.purchase_order_service import clear_po_db

client = TestClient(app)

def setup_function():
    clear_po_db()

def test_valid_purchase_order_pdf_generation():
    payload = {
        "procurement_request_id": "REQ-123",
        "vendor_id": "VEND-001",
        "category": "Hardware",
        "item_description": "Laptops",
        "quantity": 10,
        "unit_price": 1000.0,
        "selected_warranty_plan": "Extended",
        "warranty_fee": 500.0,
        "insurance_provider": "SafeInsure",
        "insurance_cost": 200.0,
        "payment_terms": "Net 30",
        "expected_delivery_date": "2026-09-01",
        "return_and_refund_policy": {
            "return_window_days": 30,
            "eligible_return_conditions": "Unopened or Defective",
            "refund_method": "Original Payment Method",
            "refund_processing_days": 7,
            "return_shipping_responsibility": "Buyer",
            "restocking_fee_percentage": 5.0,
            "non_returnable_conditions": "Physical damage by user"
        }
    }
    create_res = client.post("/api/purchase-orders/", json=payload)
    assert create_res.status_code == 200
    po_id = create_res.json()["purchase_order_id"]
    
    pdf_res = client.get(f"/api/purchase-orders/{po_id}/pdf")
    assert pdf_res.status_code == 200
    assert pdf_res.headers["content-type"] == "application/pdf"
    assert len(pdf_res.content) > 0

def test_pdf_endpoint_returns_404_for_invalid_id():
    pdf_res = client.get("/api/purchase-orders/INVALID-ID/pdf")
    assert pdf_res.status_code == 404

if __name__ == "__main__":
    setup_function()
    test_valid_purchase_order_pdf_generation()
    setup_function()
    test_pdf_endpoint_returns_404_for_invalid_id()
    print("All tests passed!")
