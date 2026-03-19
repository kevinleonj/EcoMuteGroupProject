#lab 4 ex 3
from fastapi import APIRouter, Depends, HTTPException, Header

def verify_admin_key(api_key: str = Header(...)):
    if api_key != "eco-admin-secret":
        raise HTTPException(status_code=403, detail="Forbidden")

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(verify_admin_key)]
)

@router.get("/stats")
def get_stats():
    return {"status": "admin access granted"}