# recetium backend/src/schemas/users.py
# 
# Recetium MVP 0 
# Author: Rob Palencia / Sept.2025 
# 
# Defines Pydantic models for the User entity and authentication.

from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime


class UserBase(BaseModel):
    user_email: EmailStr
    user_role: str
    user_name: Optional[str] = None
    user_phone: Optional[str] = None
    user_qr_code: Optional[str] = None
    user_is_active: Optional[bool] = True


class UserCreate(UserBase):
    user_password: str   # plain password from client


class UserUpdate(BaseModel):
    user_name: Optional[str] = None
    user_phone: Optional[str] = None
    user_password: Optional[str] = None
    user_is_active: Optional[bool] = None


class UserOut(UserBase):
    user_id: UUID
    user_created_at: datetime
    user_last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


# --- Auth ---
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
