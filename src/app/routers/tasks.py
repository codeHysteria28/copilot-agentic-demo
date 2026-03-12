"""Task management router."""

import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from src.app.dependencies import get_task_store
from src.app.models.task import TaskStatus
from src.app.schemas.task import (
    TaskCreate,
    TaskListResponse,
    TaskResponse,
    TaskUpdate,
)
from src.app.services.task_store import TaskStore

logger: logging.Logger = logging.getLogger(__name__)

router = APIRouter(prefix="/tasks", tags=["tasks"])

Store = Annotated[TaskStore, Depends(get_task_store)]


@router.get("", response_model=TaskListResponse)
async def list_tasks(
    store: Store,
    status_filter: TaskStatus | None = None,
    q: str | None = None,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> TaskListResponse:
    """List tasks with optional filtering, search, and pagination."""
    items, total = store.list_tasks(
        status=status_filter,
        query=q,
        skip=skip,
        limit=limit,
    )
    return TaskListResponse(items=items, total=total, skip=skip, limit=limit)


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    payload: TaskCreate,
    store: Store,
) -> TaskResponse:
    """Create a new task."""
    return store.create_task(payload)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: str,
    store: Store,
) -> TaskResponse:
    """Get a single task by ID."""
    task: TaskResponse | None = store.get_task(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id!r} not found",
        )
    return task


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: str,
    payload: TaskUpdate,
    store: Store,
) -> TaskResponse:
    """Partially update a task."""
    task: TaskResponse | None = store.update_task(task_id, payload)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id!r} not found",
        )
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: str,
    store: Store,
) -> Response:
    """Delete a task by ID."""
    deleted: bool = store.delete_task(task_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id!r} not found",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
