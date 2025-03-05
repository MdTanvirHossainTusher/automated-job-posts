from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def read_route():
    return {"message": "Route is working"}