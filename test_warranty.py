from fastapi.testclient import TestClient
import sys
import os
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from backend.main import app

client = TestClient(app)

def run_tests():
    print("Test 1: List warranty plans")
    res_plans = client.get("/api/warranty/plans")
    assert res_plans.status_code == 200
    plans = res_plans.json()
    assert len(plans) == 3
    plan_ids = [p["plan_id"] for p in plans]
    assert "plan_std" in plan_ids
    assert "plan_prem" in plan_ids
    print(f"Found {len(plans)} plans.")

    print("Test 2: Valid warranty creation (Standard Plan)")
    now = datetime.now(timezone.utc)
    req_data = {
        "procurement_request_id": "REQ-1",
        "vendor_id": "V-1",
        "product_or_service": "Laptops",
        "plan_id": "plan_std",
        "warranty_start_date": now.isoformat()
    }
    res = client.post("/api/warranty/", json=req_data)
    assert res.status_code == 201
    warranty = res.json()
    warranty_id = warranty["warranty_id"]
    
    assert warranty["warranty_period_months"] == 12
    assert warranty["warranty_fee"] == 0.0
    
    print("Test 3: Valid warranty creation (Premium Plan)")
    req_data_prem = {**req_data, "plan_id": "plan_prem"}
    res_prem = client.post("/api/warranty/", json=req_data_prem)
    assert res_prem.status_code == 201
    warranty_prem = res_prem.json()
    assert warranty_prem["warranty_period_months"] == 36
    assert warranty_prem["warranty_fee"] == 300.0

    print("Test 4: Reject invalid plan ID")
    req_inv = {**req_data, "plan_id": "plan_invalid"}
    res_inv = client.post("/api/warranty/", json=req_inv)
    assert res_inv.status_code == 400

    print("Test 5: EXPIRED status when expiry has passed")
    past_date = now - relativedelta(months=24)
    req_exp = {
        **req_data,
        "plan_id": "plan_std", # 12 months duration
        "warranty_start_date": past_date.isoformat()
    }
    res_exp = client.post("/api/warranty/", json=req_exp)
    assert res_exp.status_code == 201
    exp_warranty = res_exp.json()
    assert exp_warranty["status"] == "EXPIRED"
    
    print("Test 6: Retrieval works")
    res_get = client.get(f"/api/warranty/{warranty_id}")
    assert res_get.status_code == 200
    assert res_get.json()["warranty_id"] == warranty_id

    print("All warranty plan tests passed successfully!")

if __name__ == "__main__":
    run_tests()
