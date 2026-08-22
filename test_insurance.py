from fastapi.testclient import TestClient
import sys
import os
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from backend.main import app

client = TestClient(app)

def run_tests():
    now = datetime.now(timezone.utc)
    
    print("Test 1: Valid insurance creation")
    future = now + relativedelta(years=1)
    req_data = {
        "procurement_request_id": "REQ-INS",
        "vendor_id": "V-INS",
        "provider": "Global Insure",
        "policy_number": "POL-999",
        "coverage_amount": 100000.0,
        "start_date": now.isoformat(),
        "expiry_date": future.isoformat(),
        "coverage_description": "Comprehensive Liability"
    }
    res = client.post("/api/insurance/", json=req_data)
    assert res.status_code == 201
    insurance = res.json()
    
    print("Test 2: Correct provider and policy number")
    assert insurance["provider"] == "Global Insure"
    assert insurance["policy_number"] == "POL-999"
    
    print("Test 3: Coverage amount validation")
    req_inv = {**req_data, "coverage_amount": -500.0}
    res_inv = client.post("/api/insurance/", json=req_inv)
    assert res_inv.status_code == 422
    
    print("Test 4: Correct date validation")
    # Expiry before start
    req_date = {**req_data, "start_date": future.isoformat(), "expiry_date": now.isoformat()}
    res_date = client.post("/api/insurance/", json=req_date)
    assert res_date.status_code == 400
    
    print("Test 5: ACTIVE status for a valid current policy")
    assert insurance["status"] == "ACTIVE"
    
    print("Test 6: EXPIRED status for a past expiry date")
    past_start = now - relativedelta(years=2)
    past_expiry = now - relativedelta(years=1)
    req_exp = {
        **req_data,
        "start_date": past_start.isoformat(),
        "expiry_date": past_expiry.isoformat()
    }
    res_exp = client.post("/api/insurance/", json=req_exp)
    assert res_exp.status_code == 201
    assert res_exp.json()["status"] == "EXPIRED"
    
    print("Test 7: Invalid insurance ID handling")
    res_invalid_id = client.get("/api/insurance/invalid-id-123")
    assert res_invalid_id.status_code == 404
    
    print("Test 8: Deterministic behavior for identical inputs")
    res_dup = client.post("/api/insurance/", json=req_data)
    assert res_dup.status_code == 201
    insurance_dup = res_dup.json()
    assert insurance_dup["provider"] == insurance["provider"]
    assert insurance_dup["coverage_amount"] == insurance["coverage_amount"]
    assert insurance_dup["status"] == insurance["status"]
    
    print("All insurance tests passed successfully!")

if __name__ == "__main__":
    run_tests()
