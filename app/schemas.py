from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, validator


class Status(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


class User(BaseModel):
    id: int
    role: str = "user"


class TaskBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=80)
    description: Optional[str] = None
    status: Status = Status.todo
    priority: int = Field(..., ge=1, le=5)


class TaskCreate(TaskBase):
    pass


class TaskResponse(TaskBase):
    id: int
    owner_id: int


class TaskStatusUpdate(BaseModel):
    status: Status


class AdminStats(BaseModel):
    total_tasks: int
    by_status: dict[str, int]


class RoomUsersResponse(BaseModel):
    room_id: str
    users: List[str]
