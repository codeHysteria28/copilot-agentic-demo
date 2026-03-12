"""Pydantic schemas for Task request/response payloads."""

from datetime import datetime

from pydantic import BaseModel, Field

from src.app.models.task import TaskStatus


class TaskCreate(BaseModel):
    """Schema for creating a new task."""

    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(default="", max_length=1000)
    status: TaskStatus = Field(default=TaskStatus.TODO)


class TaskUpdate(BaseModel):
    """Schema for partially updating an existing task."""

    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    status: TaskStatus | None = None


class TaskResponse(BaseModel):
    """Schema returned for a single task."""

    id: str
    title: str
    description: str
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
