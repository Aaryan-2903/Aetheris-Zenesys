from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_procurement():
    return {"message": "Procurement endpoints pending implementation"}
