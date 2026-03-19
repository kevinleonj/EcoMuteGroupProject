from fastapi import APIRouter, HTTPException, Depends
from typing import List, Annotated
from src.app.models.users import UserCreate, UserResponse, UserSignup
#lab 5
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database import get_db
from src.models import User

router = APIRouter(
    prefix="/users",
    tags=["users"],
    #dependencies=[Depends(get_users_datasource)]
)

# Annotated dependency alias
#UsersDep = Annotated[UsersDataSource, Depends(get_users_datasource)]


@router.get("/", response_model=List[UserResponse])
async def read_users(
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users


@router.get("/{user_id}", response_model=UserResponse)
async def read_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.post("/", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    new_user = User(**user.model_dump())
    db.add(new_user)

    await db.commit()
    await db.refresh(new_user)

    return new_user


@router.post("/signup")
def signup(user: UserSignup):
    return {"message": "User signup validated successfully"}


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    existing = result.scalar_one_or_none()

    if not existing:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user.model_dump().items():
        setattr(existing, key, value)

    await db.commit()
    await db.refresh(existing)

    return existing


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    await db.commit()

    return {"deleted": True}