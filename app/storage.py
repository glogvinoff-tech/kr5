from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .schemas import Status, TaskResponse, TaskCreate


@dataclass
class TaskRecord:
    id: int
    title: str
    description: Optional[str]
    status: Status
    priority: int
    owner_id: int

    def to_response(self) -> TaskResponse:
        return TaskResponse(
            id=self.id,
            title=self.title,
            description=self.description,
            status=self.status,
            priority=self.priority,
            owner_id=self.owner_id,
        )


@dataclass
class TaskStorage:
    tasks: List[TaskRecord] = field(default_factory=list)
    next_id: int = 1

    def reset(self) -> None:
        self.tasks.clear()
        self.next_id = 1

    def add_task(self, owner_id: int, payload: TaskCreate) -> TaskResponse:
        task = TaskRecord(
            id=self.next_id,
            title=payload.title,
            description=payload.description,
            status=payload.status,
            priority=payload.priority,
            owner_id=owner_id,
        )
        self.tasks.append(task)
        self.next_id += 1
        return task.to_response()

    def list_tasks(self, owner_id: int, status: Optional[Status] = None, min_priority: Optional[int] = None) -> List[TaskResponse]:
        result = [task for task in self.tasks if task.owner_id == owner_id]
        if status is not None:
            result = [task for task in result if task.status == status]
        if min_priority is not None:
            result = [task for task in result if task.priority >= min_priority]
        return [task.to_response() for task in result]

    def get_task(self, task_id: int) -> Optional[TaskRecord]:
        return next((task for task in self.tasks if task.id == task_id), None)

    def update_status(self, task_id: int, status: Status) -> Optional[TaskResponse]:
        task = self.get_task(task_id)
        if task:
            task.status = status
            return task.to_response()
        return None

    def delete_task(self, task_id: int) -> bool:
        task = self.get_task(task_id)
        if task:
            self.tasks.remove(task)
            return True
        return False

    def stats(self) -> dict[str, int]:
        counts: dict[str, int] = {status.value: 0 for status in Status}
        for task in self.tasks:
            counts[task.status.value] += 1
        return counts


_storage = TaskStorage()


def get_storage() -> TaskStorage:
    return _storage
