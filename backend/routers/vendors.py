from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_vendors():
    return {"message": "Vendor endpoints pending implementation"}
