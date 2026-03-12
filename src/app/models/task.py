"""Task domain models."""

import enum


class TaskStatus(str, enum.Enum):
    """Allowed statuses for a task."""

    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
