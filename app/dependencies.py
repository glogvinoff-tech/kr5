from typing import Dict, Optional

from fastapi import Depends, Header, HTTPException, status

from .schemas import User
from .storage import get_storage


def get_current_user(x_user_id: Optional[str] = Header(None), x_user_role: Optional[str] = Header("user")) -> User:
    if x_user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="X-User-Id header missing")
    try:
        user_id = int(x_user_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid X-User-Id header")
    role = x_user_role or "user"
    return User(id=user_id, role=role)


def require_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")
    return user


def get_storage_dependency() -> Dict:
    return get_storage()
