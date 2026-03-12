"""In-memory task store with CRUD operations."""

import logging
import uuid
from datetime import datetime, timezone

from src.app.models.task import TaskStatus
from src.app.schemas.task import TaskCreate, TaskResponse, TaskUpdate

logger: logging.Logger = logging.getLogger(__name__)


class TaskStore:
    """Thread-safe in-memory storage for tasks."""

    def __init__(self) -> None:
        self._tasks: dict[str, TaskResponse] = {}

    def list_tasks(self, status: TaskStatus | None = None) -> list[TaskResponse]:
        """Return all tasks, optionally filtered by status."""
        tasks: list[TaskResponse] = list(self._tasks.values())
        if status is not None:
            tasks = [t for t in tasks if t.status == status]
        logger.info("Listed %d task(s) (filter=%s)", len(tasks), status)
        return tasks

    def create_task(self, payload: TaskCreate) -> TaskResponse:
        """Create and store a new task."""
        now: datetime = datetime.now(timezone.utc)
        task = TaskResponse(
            id=uuid.uuid4().hex,
            title=payload.title,
            description=payload.description,
            status=payload.status,
            created_at=now,
            updated_at=now,
        )
        self._tasks[task.id] = task
        logger.info("Created task %s", task.id)
        return task

    def get_task(self, task_id: str) -> TaskResponse | None:
        """Return a single task by ID, or None if not found."""
        return self._tasks.get(task_id)

    def update_task(
        self, task_id: str, payload: TaskUpdate
    ) -> TaskResponse | None:
        """Apply partial updates to an existing task."""
        existing: TaskResponse | None = self._tasks.get(task_id)
        if existing is None:
            return None

        update_data: dict[str, object] = payload.model_dump(exclude_unset=True)
        updated = existing.model_copy(
            update={**update_data, "updated_at": datetime.now(timezone.utc)},
        )
        self._tasks[task_id] = updated
        logger.info("Updated task %s", task_id)
        return updated

    def delete_task(self, task_id: str) -> bool:
        """Delete a task by ID. Returns True if deleted, False if not found."""
        if task_id in self._tasks:
            del self._tasks[task_id]
            logger.info("Deleted task %s", task_id)
            return True
        return False
