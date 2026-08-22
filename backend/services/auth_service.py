import os
import uuid
from datetime import datetime, timedelta
import jwt
import bcrypt
import sqlite3
from fastapi import HTTPException
from backend.models.schemas import UserSignup, UserLogin, UserResponse

# Configuration
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change_this_to_a_secure_random_string_in_production")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 60

DB_PATH = "auth.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Initialize DB on load
init_db()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def signup(request: UserSignup) -> UserResponse:
    user_id = str(uuid.uuid4())
    hashed_pwd = get_password_hash(request.password)
    created_at = datetime.utcnow().isoformat() + "Z"
    role = "BUYER"
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO users (user_id, name, email, password_hash, role, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, request.name, request.email, hashed_pwd, role, created_at)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="Email already registered")
    
    conn.close()
    
    return UserResponse(
        user_id=user_id,
        name=request.name,
        email=request.email,
        role=role,
        created_at=created_at
    )

def login(request: UserLogin) -> dict:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (request.email,))
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
        
    if not verify_password(request.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
        
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    
    user_response = UserResponse(
        user_id=user["user_id"],
        name=user["name"],
        email=user["email"],
        role=user["role"],
        created_at=user["created_at"]
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_response
    }

def get_current_user(token: str) -> UserResponse:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
        
    return UserResponse(
        user_id=user["user_id"],
        name=user["name"],
        email=user["email"],
        role=user["role"],
        created_at=user["created_at"]
    )
