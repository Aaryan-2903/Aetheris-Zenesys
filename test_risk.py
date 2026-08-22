from fastapi.testclient import TestClient
import sys
import json

# Add project root to path so imports work
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from backend.main import app

client = TestClient(app)

def run_tests():
    print("Testing Strong / Low-Risk Vendor...")
    res1 = client.post("/api/risk/", json={
        "vendor_id": "V-STRONG",
        "on_time_delivery_rate": 0.98,
        "defect_rate": 0.01,
        "avg_quality_score": 0.95,
        "vendor_category_spend": 80000,
        "total_category_spend": 100000,
        "advance_payment_pct": 0.0,
        "transaction_count": 25
    })
    print(f"Status: {res1.status_code}")
    print(json.dumps(res1.json(), indent=2))
    assert res1.status_code == 200

    print("\nTesting Medium-Risk Vendor...")
    res2 = client.post("/api/risk/", json={
        "vendor_id": "V-MEDIUM",
        "on_time_delivery_rate": 0.70,
        "defect_rate": 0.15,
        "avg_quality_score": 0.70,
        "vendor_category_spend": 30000,
        "total_category_spend": 100000,
        "advance_payment_pct": 0.30,
        "transaction_count": 15
    })
    print(f"Status: {res2.status_code}")
    print(json.dumps(res2.json(), indent=2))
    assert res2.status_code == 200

    print("\nTesting Weak / High-Risk Vendor...")
    res3 = client.post("/api/risk/", json={
        "vendor_id": "V-WEAK",
        "on_time_delivery_rate": 0.20,
        "defect_rate": 0.40,
        "avg_quality_score": 0.30,
        "vendor_category_spend": 5000,
        "total_category_spend": 100000,
        "advance_payment_pct": 0.80,
        "transaction_count": 3
    })
    print(f"Status: {res3.status_code}")
    print(json.dumps(res3.json(), indent=2))
    assert res3.status_code == 200

    print("\nAll tests passed successfully!")

if __name__ == "__main__":
    run_tests()
