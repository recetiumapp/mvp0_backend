# recetium backend/src/api/routes/users.py
# 
# Recetium MVP 0 
# Author: Rob Palencia / Sept.2025 
# 
# Defines API routes for managing users and authentication.

from fastapi import APIRouter, Depends, HTTPException
from typing import List
from uuid import UUID
from db.session import get_db
import crud.users as crud_users
from schemas.users import UserOut, UserCreate, UserUpdate, LoginRequest, TokenResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserOut)
async def create_user(user: UserCreate, db=Depends(get_db)):
    return await crud_users.create_user(db, user)


@router.get("/", response_model=List[UserOut])
async def list_users(db=Depends(get_db)):
    return await crud_users.get_all_users(db)


@router.get("/{user_id}", response_model=UserOut)
async def read_user(user_id: UUID, db=Depends(get_db)):
    user = await crud_users.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserOut)
async def update_user(user_id: UUID, user: UserUpdate, db=Depends(get_db)):
    updated = await crud_users.update_user(db, user_id, user)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found or no changes")
    return updated


@router.delete("/{user_id}")
async def delete_user(user_id: UUID, db=Depends(get_db)):
    deleted = await crud_users.delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}


# --- Auth ---
@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, db=Depends(get_db)):
    token = await crud_users.authenticate_user(db, request.email, request.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}
