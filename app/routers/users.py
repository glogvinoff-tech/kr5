from fastapi import APIRouter, Depends

from ..dependencies import get_current_user
from ..schemas import User

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=User)
def get_me(user: User = Depends(get_current_user)) -> User:
    return user


@router.get("/{user_id}", response_model=User)
def get_user(user_id: int, user: User = Depends(get_current_user)) -> User:
    return User(id=user_id, role=user.role)
