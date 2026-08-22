from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_risk():
    return {"message": "Risk endpoints pending implementation"}
