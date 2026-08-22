from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_financial():
    return {"message": "Financial endpoints pending implementation"}
