"""Shared test fixtures."""

import pytest
import pytest_asyncio
import httpx
from httpx import ASGITransport

from src.app.main import app
from src.app.dependencies import get_task_store
from src.app.services.task_store import TaskStore


@pytest.fixture()
def task_store() -> TaskStore:
    """Provide a fresh TaskStore for each test."""
    return TaskStore()


@pytest_asyncio.fixture()
async def client(task_store: TaskStore) -> httpx.AsyncClient:
    """Async HTTP client wired to a per-test TaskStore."""
    app.dependency_overrides[get_task_store] = lambda: task_store
    async with httpx.AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac
    app.dependency_overrides.clear()
