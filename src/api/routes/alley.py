# recetium backend/src/api/routes/alley.py
# 
# Recetium MVP 0 
# Author: Rob Palencia / Sept.2025 
# 
# Defines API routes for managing allies: list, retrieve, create, update, delete.

from fastapi import APIRouter, Depends, HTTPException
from api.deps import get_current_user, require_role
from typing import List
from uuid import UUID
from db.session import get_db
import crud.alley as crud_alley
from schemas.alley import AllyOut, AllyCreate, AllyUpdate

router = APIRouter(prefix="/allies", tags=["Allies"])


@router.get("/", response_model=List[AllyOut])
async def read_all_allies(db=Depends(get_db)):
    return await crud_alley.get_all_allies(db)

@router.get("/nearest", response_model=AllyOut)
async def get_nearest_ally(lat: float, lng: float, db=Depends(get_db)):
    ally = await crud_alley.get_nearest_ally(db, lat, lng)
    if not ally:
        raise HTTPException(status_code=404, detail="No allies found")
    return ally

@router.get("/nearest/list", response_model=list[AllyOut])
async def get_nearest_allies(lat: float, lng: float, limit: int = 5, db=Depends(get_db)):
    allies = await crud_alley.get_nearest_allies(db, lat, lng, limit)
    if not allies:
        raise HTTPException(status_code=404, detail="No allies found")
    return allies

@router.get("/{ally_id}", response_model=AllyOut)
async def read_ally(ally_id: UUID, db=Depends(get_db)):
    ally = await crud_alley.get_ally_by_id(db, ally_id)
    if not ally:
        raise HTTPException(status_code=404, detail="Ally not found")
    return ally

@router.get("/type/{ally_type}", response_model=list[AllyOut])
async def read_allies_by_type(
    ally_type: str, 
    lat: float = None, 
    lng: float = None, 
    db=Depends(get_db)
):
    return await crud_alley.get_allies_by_type(db, ally_type, lat, lng)

@router.post("/", response_model=AllyOut)
async def create_new_ally(ally: AllyCreate, db=Depends(get_db)):
    return await crud_alley.create_ally(db, ally)


@router.put("/{ally_id}", response_model=AllyOut)
async def update_existing_ally(ally_id: UUID, ally: AllyUpdate, db=Depends(get_db)):
    updated = await crud_alley.update_ally(db, ally_id, ally)
    if not updated:
        raise HTTPException(status_code=404, detail="Ally not found or no changes")
    return updated


@router.delete("/{ally_id}")
async def delete_existing_ally(ally_id: UUID, db=Depends(get_db)):
    deleted = await crud_alley.delete_ally(db, ally_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Ally not found")
    return {"message": "Ally deleted successfully"}

@router.get("/search/", response_model=list[AllyOut])
async def search_allies_by_name(
    name: str,
    lat: float = None,
    lng: float = None,
    db=Depends(get_db)
):
    return await crud_alley.get_allies_by_name(db, name, lat, lng)
