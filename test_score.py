import json
from fastapi.testclient import TestClient
from backend.main import app
import os

# Ensure dummy env vars are set so supabase client doesn't complain during import
os.environ["SUPABASE_URL"] = "http://dummy.url"
os.environ["SUPABASE_KEY"] = "dummy_key"

client = TestClient(app)

def test_score():
    print("Testing /api/score...")
    
    payload = {
        "budget_per_unit": 50000.0,
        "required_lead_time": 30,
        "vendors": [
            {
                "vendor_id": "V001",
                "on_time_delivery_rate": 0.85,
                "avg_quality_score": 0.90,
                "vendor_price": 45000.0,
                "actual_lead_time": 25,
                "payment_terms_days": 60
            },
            {
                "vendor_id": "V002",
                "on_time_delivery_rate": 0.95,
                "avg_quality_score": 0.95,
                "vendor_price": 55000.0,
                "actual_lead_time": 35,
                "payment_terms_days": 30
            },
            {
                "vendor_id": "V003",
                "on_time_delivery_rate": 0.60,
                "avg_quality_score": 0.70,
                "vendor_price": 40000.0,
                "actual_lead_time": 20,
                "payment_terms_days": 15
            }
        ]
    }
    
    response = client.post("/api/score/", json=payload)
    if response.status_code != 200:
        print(f"Request failed: {response.status_code} {response.text}")
        return
        
    result = response.json()
    print("Score Response:")
    print(json.dumps(result, indent=2))
    print("\nRanking:")
    for rank, v in enumerate(result['ranked_vendors'], 1):
        print(f" {rank}. {v['vendor_id']} - Final Score: {v['final_score']:.4f}")

if __name__ == "__main__":
    test_score()
