from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from backend.main import app

client = TestClient(app)

def run_tests():
    print("Test 1: 0% repeat ratio")
    res_0 = client.post("/api/repeat-ratio/", json={
        "vendor_id": "V-001",
        "total_orders": 100,
        "repeat_orders": 0
    })
    assert res_0.status_code == 200
    assert res_0.json()["order_repeat_ratio"] == 0.0
    assert res_0.json()["interpretation"] == "Low"

    print("Test 2: 50% repeat ratio")
    res_50 = client.post("/api/repeat-ratio/", json={
        "vendor_id": "V-002",
        "total_orders": 100,
        "repeat_orders": 50
    })
    assert res_50.status_code == 200
    assert res_50.json()["order_repeat_ratio"] == 50.0
    assert res_50.json()["interpretation"] == "Moderate"

    print("Test 3: 65% repeat ratio")
    res_65 = client.post("/api/repeat-ratio/", json={
        "vendor_id": "V-003",
        "total_orders": 100,
        "repeat_orders": 65
    })
    assert res_65.status_code == 200
    assert res_65.json()["order_repeat_ratio"] == 65.0
    assert res_65.json()["interpretation"] == "High"

    print("Test 4: 100% repeat ratio")
    res_100 = client.post("/api/repeat-ratio/", json={
        "vendor_id": "V-004",
        "total_orders": 100,
        "repeat_orders": 100
    })
    assert res_100.status_code == 200
    assert res_100.json()["order_repeat_ratio"] == 100.0
    assert res_100.json()["interpretation"] == "Very High"

    print("Test 5: repeat_orders > total_orders is rejected")
    res_gt = client.post("/api/repeat-ratio/", json={
        "vendor_id": "V-005",
        "total_orders": 100,
        "repeat_orders": 105
    })
    assert res_gt.status_code == 400

    print("Test 6: negative repeat_orders is rejected")
    res_neg = client.post("/api/repeat-ratio/", json={
        "vendor_id": "V-006",
        "total_orders": 100,
        "repeat_orders": -5
    })
    assert res_neg.status_code == 422

    print("Test 7: total_orders = 0 is rejected")
    res_zero_tot = client.post("/api/repeat-ratio/", json={
        "vendor_id": "V-007",
        "total_orders": 0,
        "repeat_orders": 0
    })
    assert res_zero_tot.status_code == 422

    print("Test 8: correct interpretation is returned (covered in 1-4)")

    print("Test 9: deterministic result for identical inputs")
    res_dup = client.post("/api/repeat-ratio/", json={
        "vendor_id": "V-003",
        "total_orders": 100,
        "repeat_orders": 65
    })
    assert res_dup.json() == res_65.json()

    print("Test 10: valid vendor ID handling")
    res_get = client.get("/api/repeat-ratio/V-003")
    assert res_get.status_code == 200
    assert res_get.json()["vendor_id"] == "V-003"
    
    res_get_inv = client.get("/api/repeat-ratio/V-UNKNOWN")
    assert res_get_inv.status_code == 404

    print("All tests passed successfully!")

if __name__ == "__main__":
    run_tests()
