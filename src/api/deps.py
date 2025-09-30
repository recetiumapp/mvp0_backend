# recetium backend/src/api/deps.py
#
# Recetium MVP 0
# Author: Rob Palencia / Sept.2025
#
# Security dependencies for role-based access control.

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from core.security import decode_access_token
from db.session import get_db
import crud.users as crud_users

# Use HTTPBearer instead of OAuth2PasswordBearer
bearer_scheme = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db=Depends(get_db)
):
    """
    Extract user from JWT Bearer token and fetch from DB.
    """
    token = credentials.credentials
    payload = decode_access_token(token)

    if payload is None or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    user_id = payload["sub"]
    user = await crud_users.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


def require_role(*allowed_roles: str):
    """
    Returns a dependency function that validates user role.
    Example: Depends(require_role("admin", "backoffice"))
    """
    async def role_checker(current_user=Depends(get_current_user)):
        if current_user["user_role"] not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation not permitted for role {current_user['user_role']}",
            )
        return current_user
    return role_checker
