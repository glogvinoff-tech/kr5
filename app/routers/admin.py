from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies import get_storage_dependency, require_admin
from ..schemas import AdminStats, User
from ..storage import TaskStorage

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/stats", response_model=AdminStats)
def get_stats(
    user: User = Depends(require_admin),
    storage: TaskStorage = Depends(get_storage_dependency),
) -> AdminStats:
    counts = storage.stats()
    return AdminStats(total_tasks=len(storage.tasks), by_status=counts)


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    user: User = Depends(require_admin),
    storage: TaskStorage = Depends(get_storage_dependency),
) -> None:
    task = storage.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    storage.delete_task(task_id)
