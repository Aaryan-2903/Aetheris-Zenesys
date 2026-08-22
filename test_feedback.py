from fastapi.testclient import TestClient
from backend.main import app
from backend.services.feedback_service import clear_feedback_db

client = TestClient(app)

def setup_function():
    clear_feedback_db()

def test_valid_feedback_creation():
    payload = {
        "order_id": "ORD-001",
        "vendor_id": "VEND-001",
        "overall_rating": 4,
        "quality_rating": 5,
        "delivery_rating": 4,
        "responsiveness_rating": 3,
        "comments": "Good vendor"
    }
    response = client.post("/api/feedback/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["order_id"] == "ORD-001"
    assert data["vendor_id"] == "VEND-001"
    assert data["overall_rating"] == 4
    assert "feedback_id" in data

def test_overall_rating_validation():
    payload = {
        "order_id": "ORD-001",
        "vendor_id": "VEND-001",
        "overall_rating": 6,
        "quality_rating": 5,
        "delivery_rating": 4,
        "responsiveness_rating": 3
    }
    response = client.post("/api/feedback/", json=payload)
    assert response.status_code == 422
    
def test_quality_rating_validation():
    payload = {
        "order_id": "ORD-001",
        "vendor_id": "VEND-001",
        "overall_rating": 4,
        "quality_rating": 0,
        "delivery_rating": 4,
        "responsiveness_rating": 3
    }
    response = client.post("/api/feedback/", json=payload)
    assert response.status_code == 422
    
def test_delivery_rating_validation():
    payload = {
        "order_id": "ORD-001",
        "vendor_id": "VEND-001",
        "overall_rating": 4,
        "quality_rating": 4,
        "delivery_rating": 6,
        "responsiveness_rating": 3
    }
    response = client.post("/api/feedback/", json=payload)
    assert response.status_code == 422

def test_responsiveness_rating_validation():
    payload = {
        "order_id": "ORD-001",
        "vendor_id": "VEND-001",
        "overall_rating": 4,
        "quality_rating": 4,
        "delivery_rating": 4,
        "responsiveness_rating": -1
    }
    response = client.post("/api/feedback/", json=payload)
    assert response.status_code == 422

def test_missing_required_fields():
    payload = {
        "overall_rating": 4,
        "quality_rating": 5,
        "delivery_rating": 4,
        "responsiveness_rating": 3
    }
    response = client.post("/api/feedback/", json=payload)
    assert response.status_code == 422
    
def test_optional_comments():
    payload = {
        "order_id": "ORD-001",
        "vendor_id": "VEND-001",
        "overall_rating": 4,
        "quality_rating": 5,
        "delivery_rating": 4,
        "responsiveness_rating": 3
        # comments missing
    }
    response = client.post("/api/feedback/", json=payload)
    assert response.status_code == 200

def test_vendor_feedback_summary():
    # Submit 2 feedbacks for same vendor
    payload1 = {
        "order_id": "ORD-001",
        "vendor_id": "VEND-001",
        "overall_rating": 4,
        "quality_rating": 5,
        "delivery_rating": 4,
        "responsiveness_rating": 3
    }
    payload2 = {
        "order_id": "ORD-002",
        "vendor_id": "VEND-001",
        "overall_rating": 2,
        "quality_rating": 3,
        "delivery_rating": 2,
        "responsiveness_rating": 1
    }
    client.post("/api/feedback/", json=payload1)
    client.post("/api/feedback/", json=payload2)
    
    response = client.get("/api/feedback/vendor/VEND-001")
    assert response.status_code == 200
    data = response.json()
    
    assert data["feedback_count"] == 2
    assert data["average_overall_rating"] == 3.0
    assert data["average_quality_rating"] == 4.0
    assert data["average_delivery_rating"] == 3.0
    assert data["average_responsiveness_rating"] == 2.0

def test_average_ratings_are_calculated_correctly():
    payload1 = {
        "order_id": "ORD-003",
        "vendor_id": "VEND-002",
        "overall_rating": 5,
        "quality_rating": 5,
        "delivery_rating": 5,
        "responsiveness_rating": 5
    }
    payload2 = {
        "order_id": "ORD-004",
        "vendor_id": "VEND-002",
        "overall_rating": 4,
        "quality_rating": 4,
        "delivery_rating": 4,
        "responsiveness_rating": 4
    }
    client.post("/api/feedback/", json=payload1)
    client.post("/api/feedback/", json=payload2)
    
    response = client.get("/api/feedback/vendor/VEND-002")
    assert response.status_code == 200
    data = response.json()
    
    assert data["feedback_count"] == 2
    assert data["average_overall_rating"] == 4.5
    
def test_empty_vendor_feedback_state():
    response = client.get("/api/feedback/vendor/VEND-UNKNOWN")
    assert response.status_code == 200
    data = response.json()
    assert data["feedback_count"] == 0
    assert data["average_overall_rating"] == 0.0

def test_deterministic_results():
    payload1 = {
        "order_id": "ORD-001",
        "vendor_id": "VEND-001",
        "overall_rating": 4,
        "quality_rating": 5,
        "delivery_rating": 4,
        "responsiveness_rating": 3
    }
    client.post("/api/feedback/", json=payload1)
    
    res1 = client.get("/api/feedback/vendor/VEND-001").json()
    res2 = client.get("/api/feedback/vendor/VEND-001").json()
    
    assert res1 == res2

if __name__ == "__main__":
    setup_function()
    test_valid_feedback_creation()
    setup_function()
    test_overall_rating_validation()
    setup_function()
    test_quality_rating_validation()
    setup_function()
    test_delivery_rating_validation()
    setup_function()
    test_responsiveness_rating_validation()
    setup_function()
    test_missing_required_fields()
    setup_function()
    test_optional_comments()
    setup_function()
    test_vendor_feedback_summary()
    setup_function()
    test_average_ratings_are_calculated_correctly()
    setup_function()
    test_empty_vendor_feedback_state()
    setup_function()
    test_deterministic_results()
    print("All tests passed!")
