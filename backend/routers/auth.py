from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from backend.models.schemas import UserSignup, UserLogin, UserResponse, Token
from backend.services.auth_service import signup, login, get_current_user

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

@router.post("/signup", response_model=UserResponse)
def signup_endpoint(request: UserSignup):
    return signup(request)

@router.post("/login", response_model=Token)
def login_endpoint(request: UserLogin):
    return login(request)

@router.get("/me", response_model=UserResponse)
def read_users_me(token: str = Depends(oauth2_scheme)):
    return get_current_user(token)
