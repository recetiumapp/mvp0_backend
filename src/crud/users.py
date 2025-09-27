# recetium backend/src/crud/users.py
# 
# Recetium MVP 0 
# Author: Rob Palencia / Sept.2025 
# 
# Implements CRUD operations for the User model and authentication.

from typing import List, Optional
from uuid import UUID
from db.session import get_db
from schemas.users import UserCreate, UserUpdate
from core.security import hash_password, verify_password, create_access_token
from decimal import Decimal


def row_to_dict(row):
    d = dict(row)
    for k, v in d.items():
        if isinstance(v, Decimal):
            d[k] = float(v)
    return d


async def create_user(db, user: UserCreate) -> dict:
    query = """
        INSERT INTO users (user_email, user_password_hash, user_role, user_name, user_phone, user_qr_code)
        VALUES ($1, $2, $3, $4, $5, $6)
        RETURNING *
    """
    row = await db.fetchrow(
        query,
        user.user_email,
        hash_password(user.user_password),
        user.user_role,
        user.user_name,
        user.user_phone,
        user.user_qr_code
    )
    return row_to_dict(row)


async def get_user_by_email(db, email: str) -> Optional[dict]:
    row = await db.fetchrow("SELECT * FROM users WHERE user_email = $1", email)
    return row_to_dict(row) if row else None


async def get_user_by_id(db, user_id: UUID) -> Optional[dict]:
    row = await db.fetchrow("SELECT * FROM users WHERE user_id = $1", user_id)
    return row_to_dict(row) if row else None


async def get_all_users(db) -> List[dict]:
    rows = await db.fetch("SELECT * FROM users")
    return [row_to_dict(r) for r in rows]


async def update_user(db, user_id: UUID, user: UserUpdate) -> Optional[dict]:
    update_fields = user.dict(exclude_unset=True)
    if "user_password" in update_fields:
        update_fields["user_password_hash"] = hash_password(update_fields.pop("user_password"))

    if not update_fields:
        return None

    set_clause = ", ".join([f"{k} = ${i+2}" for i, k in enumerate(update_fields.keys())])
    values = list(update_fields.values())

    query = f"UPDATE users SET {set_clause}, user_last_login = user_last_login WHERE user_id = $1 RETURNING *"
    row = await db.fetchrow(query, user_id, *values)
    return row_to_dict(row) if row else None


async def delete_user(db, user_id: UUID) -> bool:
    result = await db.execute("DELETE FROM users WHERE user_id = $1", user_id)
    return result == "DELETE 1"


# --- Auth ---
async def authenticate_user(db, email: str, password: str) -> Optional[str]:
    user = await get_user_by_email(db, email)
    if not user or not verify_password(password, user["user_password_hash"]):
        return None
    # update last login
    await db.execute("UPDATE users SET user_last_login = now() WHERE user_id = $1", user["user_id"])
    token = create_access_token({"sub": str(user["user_id"]), "role": user["user_role"]})
    return token
