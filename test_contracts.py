from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from backend.main import app
from backend.services.contract_service import _contracts

client = TestClient(app)

def run_tests():
    print("Test 1: Contract creation returns HTTP 201")
    req_data = {
        "procurement_request_id": "REQ-123",
        "vendor_id": "V-456",
        "buyer_terms": "Standard Net 30",
        "vendor_terms": "Agree to Net 30",
        "payment_terms": "Net 30",
        "delivery_terms": "FOB Destination",
        "warranty_terms": "1 Year",
        "return_replacement_terms": "30 days no questions",
        "compliance_requirements": "ISO 9001",
        "buyer_code_of_conduct": "Standard CoC",
        "vendor_code_of_conduct": "Agreed CoC"
    }
    res = client.post("/api/contracts/", json=req_data)
    assert res.status_code == 201
    contract = res.json()
    contract_id = contract["contract_id"]
    
    print("Test 2: Initial status is PENDING_ACCEPTANCE")
    assert contract["status"] == "PENDING_ACCEPTANCE"
    assert contract["buyer_accepted"] == False
    assert contract["vendor_accepted"] == False
    assert contract["accepted_at"] is None
    
    print("Test 3: Buyer acceptance works")
    res_b = client.post(f"/api/contracts/{contract_id}/accept/buyer")
    assert res_b.status_code == 200
    contract_b = res_b.json()
    assert contract_b["buyer_accepted"] == True
    assert contract_b["vendor_accepted"] == False
    assert contract_b["status"] == "PENDING_ACCEPTANCE"
    
    print("Test 4: Vendor acceptance works & Contract becomes ACCEPTED")
    res_v = client.post(f"/api/contracts/{contract_id}/accept/vendor")
    assert res_v.status_code == 200
    contract_v = res_v.json()
    assert contract_v["buyer_accepted"] == True
    assert contract_v["vendor_accepted"] == True
    
    print("Test 5: Contract becomes ACCEPTED only after both accept")
    assert contract_v["status"] == "ACCEPTED"
    
    print("Test 6: accepted_at is populated only after both accept")
    assert contract_v["accepted_at"] is not None
    
    print("Test 7: Invalid contract ID is handled correctly")
    res_inv = client.post("/api/contracts/invalid-123/accept/buyer")
    assert res_inv.status_code == 404
    
    print("Test 8: Expired contract cannot be accepted")
    # Manually expire a new contract for testing
    res_exp = client.post("/api/contracts/", json=req_data)
    exp_id = res_exp.json()["contract_id"]
    _contracts[exp_id].status = "EXPIRED"
    
    res_exp_acc = client.post(f"/api/contracts/{exp_id}/accept/buyer")
    assert res_exp_acc.status_code == 400
    assert "Cannot accept an expired contract" in res_exp_acc.json()["detail"]

    print("All tests passed successfully!")

if __name__ == "__main__":
    run_tests()
