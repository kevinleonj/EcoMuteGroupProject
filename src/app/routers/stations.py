from fastapi import APIRouter, Depends, HTTPException
from src.app.dependencies import get_current_user

router = APIRouter(prefix="/stations", tags=["stations"])


@router.post("/")
async def create_station(current_user = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")

    return {"message": "Station created successfully"}