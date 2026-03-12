"""FastAPI dependency providers."""

from src.app.services.task_store import TaskStore

_task_store = TaskStore()


def get_task_store() -> TaskStore:
    """Provide the singleton TaskStore instance."""
    return _task_store
