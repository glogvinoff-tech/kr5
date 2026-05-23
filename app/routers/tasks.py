from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from ..dependencies import get_current_user, get_storage_dependency
from ..schemas import TaskCreate, TaskResponse, TaskStatusUpdate, Status, User
from ..storage import TaskRecord, TaskStorage

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreate,
    user: User = Depends(get_current_user),
    storage: TaskStorage = Depends(get_storage_dependency),
) -> TaskResponse:
    return storage.add_task(owner_id=user.id, payload=payload)


@router.get("", response_model=List[TaskResponse])
def list_tasks(
    status: Optional[Status] = Query(None),
    min_priority: Optional[int] = Query(None, ge=1, le=5),
    user: User = Depends(get_current_user),
    storage: TaskStorage = Depends(get_storage_dependency),
) -> List[TaskResponse]:
    return storage.list_tasks(owner_id=user.id, status=status, min_priority=min_priority)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    user: User = Depends(get_current_user),
    storage: TaskStorage = Depends(get_storage_dependency),
) -> TaskResponse:
    task = storage.get_task(task_id)
    if task is None or task.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task.to_response()


@router.patch("/{task_id}/status", response_model=TaskResponse)
def update_task_status(
    task_id: int,
    payload: TaskStatusUpdate,
    user: User = Depends(get_current_user),
    storage: TaskStorage = Depends(get_storage_dependency),
) -> TaskResponse:
    task = storage.get_task(task_id)
    if task is None or task.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    updated = storage.update_status(task_id=task_id, status=payload.status)
    assert updated is not None
    return updated


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    user: User = Depends(get_current_user),
    storage: TaskStorage = Depends(get_storage_dependency),
) -> Response:
    task = storage.get_task(task_id)
    if task is None or task.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    storage.delete_task(task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
