import os
import sqlite3

# Clean up db before tests
if os.path.exists("auth.db"):
    os.remove("auth.db")

from fastapi.testclient import TestClient
from backend.main import app
from backend.services.auth_service import init_db

init_db()

client = TestClient(app)

def test_auth_signup_successful():
    response = client.post("/api/auth/signup", json={
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "strongpassword123"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test User"
    assert data["email"] == "testuser@example.com"
    assert data["role"] == "BUYER"
    assert "user_id" in data
    assert "password" not in data
    assert "password_hash" not in data

def test_auth_signup_duplicate_email():
    response = client.post("/api/auth/signup", json={
        "name": "Another User",
        "email": "testuser@example.com",
        "password": "anotherpassword123"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_auth_signup_invalid_email():
    response = client.post("/api/auth/signup", json={
        "name": "Bad Email",
        "email": "not-an-email",
        "password": "strongpassword123"
    })
    assert response.status_code == 422 # Pydantic validation error

def test_auth_signup_invalid_password():
    response = client.post("/api/auth/signup", json={
        "name": "Short Pass",
        "email": "short@example.com",
        "password": "short" # Needs to be min 8
    })
    assert response.status_code == 422

def test_auth_login_successful():
    response = client.post("/api/auth/login", json={
        "email": "testuser@example.com",
        "password": "strongpassword123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "user" in data
    user = data["user"]
    assert user["email"] == "testuser@example.com"
    assert user["role"] == "BUYER"
    assert "password" not in user
    assert "password_hash" not in user

def test_auth_login_invalid_password():
    response = client.post("/api/auth/login", json={
        "email": "testuser@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"

def test_auth_login_invalid_email():
    response = client.post("/api/auth/login", json={
        "email": "wrong@example.com",
        "password": "strongpassword123"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"

def test_auth_me_valid_token():
    # Login first
    login_res = client.post("/api/auth/login", json={
        "email": "testuser@example.com",
        "password": "strongpassword123"
    })
    token = login_res.json()["access_token"]
    
    # Get me
    me_res = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_res.status_code == 200
    user = me_res.json()
    assert user["email"] == "testuser@example.com"
    assert "password" not in user
    assert "password_hash" not in user

def test_auth_me_without_token():
    me_res = client.get("/api/auth/me")
    assert me_res.status_code == 401
    assert me_res.json()["detail"] == "Not authenticated"

def test_auth_me_invalid_token():
    me_res = client.get("/api/auth/me", headers={"Authorization": "Bearer invalid.token.here"})
    assert me_res.status_code == 401
    assert me_res.json()["detail"] == "Invalid token"

def test_deterministic_behavior():
    # Logging in multiple times gives a token and consistent user shape
    for _ in range(3):
        res = client.post("/api/auth/login", json={
            "email": "testuser@example.com",
            "password": "strongpassword123"
        })
        assert res.status_code == 200
        assert "access_token" in res.json()

def test_sqlite_persistence():
    # Force a direct connection to the database independently
    # to verify the user exists persistently outside of the running process cache
    conn = sqlite3.connect("auth.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", ("testuser@example.com",))
    user = cursor.fetchone()
    conn.close()
    
    assert user is not None
    assert user["email"] == "testuser@example.com"
    assert user["role"] == "BUYER"
    
    # Also verify login still works
    res = client.post("/api/auth/login", json={
        "email": "testuser@example.com",
        "password": "strongpassword123"
    })
    assert res.status_code == 200

if __name__ == "__main__":
    test_auth_signup_successful()
    test_auth_signup_duplicate_email()
    test_auth_signup_invalid_email()
    test_auth_signup_invalid_password()
    test_auth_login_successful()
    test_auth_login_invalid_password()
    test_auth_login_invalid_email()
    test_auth_me_valid_token()
    test_auth_me_without_token()
    test_auth_me_invalid_token()
    test_deterministic_behavior()
    test_sqlite_persistence()
    print("All auth tests passed!")


