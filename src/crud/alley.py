# recetium backend/src/crud/alley.py
# 
# Recetium MVP 0 
# Author: Rob Palencia / Sept.2025 
# 
# Implements CRUD operations for the Ally model. Handles direct interaction with 
# the allies table in the database.

from typing import List, Optional
from uuid import UUID
from decimal import Decimal
from db.session import get_db
from schemas.alley import AllyCreate, AllyUpdate


def row_to_dict(row):
    """Convert asyncpg.Record to dict and Decimal → float."""
    d = dict(row)
    for k, v in d.items():
        if isinstance(v, Decimal):
            d[k] = float(v)
    return d


async def get_all_allies(db) -> List[dict]:
    rows = await db.fetch("SELECT * FROM allies")
    return [row_to_dict(r) for r in rows]


async def get_ally_by_id(db, ally_id: UUID) -> Optional[dict]:
    row = await db.fetchrow("SELECT * FROM allies WHERE ally_id = $1", ally_id)
    return row_to_dict(row) if row else None


async def get_allies_by_type(db, ally_type: str, lat: float = None, lng: float = None) -> list[dict]:
    if lat is not None and lng is not None:
        query = """
            SELECT *,
                   ( 6371 * acos(
                        cos(radians($1)) * cos(radians(ally_lat)) *
                        cos(radians(ally_lng) - radians($2)) +
                        sin(radians($1)) * sin(radians(ally_lat))
                   )) AS distance_km
            FROM allies
            WHERE ally_type = $3
            ORDER BY distance_km ASC
        """
        rows = await db.fetch(query, lat, lng, ally_type)
    else:
        query = "SELECT * FROM allies WHERE ally_type = $1"
        rows = await db.fetch(query, ally_type)

    return [row_to_dict(r) for r in rows]


async def create_ally(db, ally: AllyCreate) -> dict:
    query = """
        INSERT INTO allies (
            ally_user_id, ally_type, ally_name, ally_description, ally_address,
            ally_lat, ally_lng, ally_schedule
        ) VALUES ($1,$2,$3,$4,$5,$6,$7,$8)
        RETURNING *
    """
    row = await db.fetchrow(
        query,
        ally.ally_user_id,
        ally.ally_type,
        ally.ally_name,
        ally.ally_description,
        ally.ally_address,
        ally.ally_lat,
        ally.ally_lng,
        ally.ally_schedule,
    )
    return row_to_dict(row)


async def update_ally(db, ally_id: UUID, ally: AllyUpdate) -> Optional[dict]:
    update_fields = ally.dict(exclude_unset=True)
    if not update_fields:
        return None

    set_clause = ", ".join([f"{k} = ${i+2}" for i, k in enumerate(update_fields.keys())])
    values = list(update_fields.values())

    query = f"UPDATE allies SET {set_clause} WHERE ally_id = $1 RETURNING *"
    row = await db.fetchrow(query, ally_id, *values)
    return row_to_dict(row) if row else None


async def delete_ally(db, ally_id: UUID) -> bool:
    result = await db.execute("DELETE FROM allies WHERE ally_id = $1", ally_id)
    return result == "DELETE 1"

async def get_allies_by_name(db, name: str, lat: float = None, lng: float = None) -> list[dict]:
    if lat is not None and lng is not None:
        query = """
            SELECT *,
                   ( 6371 * acos(
                        cos(radians($1)) * cos(radians(ally_lat)) *
                        cos(radians(ally_lng) - radians($2)) +
                        sin(radians($1)) * sin(radians(ally_lat))
                   )) AS distance_km
            FROM allies
            WHERE ally_name ILIKE $3
            ORDER BY distance_km ASC
        """
        rows = await db.fetch(query, lat, lng, f"%{name}%")
    else:
        query = "SELECT * FROM allies WHERE ally_name ILIKE $1"
        rows = await db.fetch(query, f"%{name}%")

    return [row_to_dict(r) for r in rows]

async def get_nearest_ally(db, lat: float, lng: float) -> dict:
    query = """
        SELECT *,
               ( 6371 * acos(
                    cos(radians($1)) * cos(radians(ally_lat)) *
                    cos(radians(ally_lng) - radians($2)) +
                    sin(radians($1)) * sin(radians(ally_lat))
               )) AS distance_km
        FROM allies
        ORDER BY distance_km ASC
        LIMIT 1
    """
    row = await db.fetchrow(query, lat, lng)
    return row_to_dict(row) if row else None

async def get_nearest_allies(db, lat: float, lng: float, limit: int = 5) -> list[dict]:
    query = """
        SELECT *,
               ( 6371 * acos(
                    cos(radians($1)) * cos(radians(ally_lat)) *
                    cos(radians(ally_lng) - radians($2)) +
                    sin(radians($1)) * sin(radians(ally_lat))
               )) AS distance_km
        FROM allies
        ORDER BY distance_km ASC
        LIMIT $3
    """
    rows = await db.fetch(query, lat, lng, limit)
    return [row_to_dict(r) for r in rows]
