"""FastAPI application entry point."""

import logging

from fastapi import FastAPI

from src.app.routers import tasks

logging.basicConfig(level=logging.INFO)

app: FastAPI = FastAPI(
    title="Task Management API",
    version="0.1.0",
)

app.include_router(tasks.router)
