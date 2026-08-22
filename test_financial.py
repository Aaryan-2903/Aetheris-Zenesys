from fastapi.testclient import TestClient
import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from backend.main import app

client = TestClient(app)

def run_tests():
    print("Testing Strong vendor / low-risk procurement...")
    res1 = client.post("/api/financial/", json={
        "purchase_value": 100000.0,
        "advance_payment_pct": 0.0,
        "historical_price_stddev": 5.0,
        "historical_avg_price": 100.0,
        "transaction_count": 20,
        "supplier_health_score": 0.90,
        "payment_risk_score": 0.0,
        "delivery_risk_score": 0.05,
        "quality_risk_score": 0.02
    })
    print(f"Status: {res1.status_code}")
    print(json.dumps(res1.json(), indent=2))
    assert res1.status_code == 200
    data1 = res1.json()
    assert data1["price_risk_exposure"] == (100000.0 * (5/100) * 0.5)
    assert data1["total_money_at_risk"] > 0
    
    print("\nTesting Medium-risk procurement...")
    res2 = client.post("/api/financial/", json={
        "purchase_value": 50000.0,
        "advance_payment_pct": 0.30,
        "historical_price_stddev": 15.0,
        "historical_avg_price": 100.0,
        "transaction_count": 10,
        "supplier_health_score": 0.60,
        "payment_risk_score": 0.20,
        "delivery_risk_score": 0.30,
        "quality_risk_score": 0.25
    })
    print(f"Status: {res2.status_code}")
    print(json.dumps(res2.json(), indent=2))
    assert res2.status_code == 200

    print("\nTesting Weak/high-risk procurement...")
    res3 = client.post("/api/financial/", json={
        "purchase_value": 200000.0,
        "advance_payment_pct": 0.50,
        "historical_price_stddev": 0.0,
        "historical_avg_price": 0.0,
        "transaction_count": 2,
        "supplier_health_score": 0.20,
        "payment_risk_score": 0.80,
        "delivery_risk_score": 0.70,
        "quality_risk_score": 0.60
    })
    print(f"Status: {res3.status_code}")
    print(json.dumps(res3.json(), indent=2))
    assert res3.status_code == 200
    data3 = res3.json()
    assert data3["is_low_confidence_price"] == True
    assert data3["price_risk_exposure"] == 0.0
    
    # Check that high risk means higher percentage exposure
    assert data3["exposure_percentage"] > data1["exposure_percentage"]

    print("\nAll tests passed successfully!")

if __name__ == "__main__":
    run_tests()
