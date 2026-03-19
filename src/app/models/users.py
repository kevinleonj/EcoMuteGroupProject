# LAB 5 UPDATE:
# This Pydantic model was refactored to align with the SQLAlchemy User model.
# The previous fields (username, is_active) were removed to ensure consistency
# between the API schema and the database schema (name, email).
# This prevents schema mismatches and supports proper ORM serialization.

from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

class UserSignup(BaseModel):
    name: str
    email: EmailStr
    password: str