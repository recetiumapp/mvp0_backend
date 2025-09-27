# recetium backend/src/schemas/alley.py
# 
# Recetium MVP 0 
# Author: Rob Palencia / Sept.2025 
# 
# Defines Pydantic models for the Ally entity (input/output validation).

from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime


class AllyBase(BaseModel):
    ally_type: str
    ally_name: str
    ally_description: Optional[str] = None
    ally_address: Optional[str] = None
    ally_lat: Optional[float] = None
    ally_lng: Optional[float] = None
    ally_schedule: Optional[str] = None


class AllyCreate(AllyBase):
    ally_user_id: UUID


class AllyUpdate(BaseModel):
    ally_name: Optional[str] = None
    ally_description: Optional[str] = None
    ally_address: Optional[str] = None
    ally_schedule: Optional[str] = None


class AllyOut(AllyBase):
    ally_id: UUID
    ally_user_id: UUID
    ally_rating_avg: Optional[float] = 0.0
    ally_promoted: Optional[bool] = False
    ally_status: Optional[str] = "draft"
    ally_created_at: datetime
    distance_km: Optional[float] = None   # 👈 agregado

    class Config:
        from_attributes = True
