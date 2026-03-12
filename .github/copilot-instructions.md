# Copilot Instructions — Task Management API

## Project Overview

This is a **Task Management API** built with Python and FastAPI.

## Tech Stack

- **Python** 3.14.2
- **FastAPI** as the web framework
- **Pydantic v2** for data validation and serialization
- **pytest** and **httpx** for testing

## Project Structure

```
src/
  app/
    __init__.py
    main.py
    routers/
    models/
    schemas/
    services/
    dependencies.py
tests/
  __init__.py
  conftest.py
requirements.txt
```

- Application code lives in `src/app/`.
- Tests live in the top-level `tests/` directory.

## Code Style & Conventions

- Follow the **Google Python Style Guide**.
- Add **type hints to all** function signatures, variables, and return types.
- Use `snake_case` for functions, methods, and variables. Use `PascalCase` for classes.
- Keep functions short and focused on a single responsibility.

## Logging

- **Never use `print()` for logging.** Always use the Python `logging` module.
- Obtain loggers via `logging.getLogger(__name__)`.

## API & Data Rules

- **All endpoints must return Pydantic models**, never raw `dict` objects.
- Define request and response schemas as Pydantic v2 `BaseModel` subclasses in `src/app/schemas/`.
- Use Pydantic's `model_validator`, `field_validator`, and `Field()` for validation — not manual checks.
- Use `Annotated` types with FastAPI's `Depends()` for dependency injection.

## Testing

- Write tests with **pytest** and use **httpx.AsyncClient** (via `ASGITransport`) for async endpoint testing.
- Place all tests in the `tests/` directory, mirroring the `src/app/` structure.
- Name test files `test_<module>.py` and test functions `test_<behavior>`.
- Use fixtures in `conftest.py` for shared setup (e.g., test client, database sessions).

## Error Handling

- Raise `fastapi.HTTPException` with appropriate status codes for expected errors.
- Use custom exception handlers registered on the FastAPI app for domain-specific errors.
- Return error responses as Pydantic models with a consistent shape (e.g., `detail` field).

## General

- Prefer `async def` for route handlers and I/O-bound operations.
- Keep business logic in `src/app/services/`, not in route handlers directly.
- Use environment variables (via Pydantic `BaseSettings`) for configuration — never hard-code secrets.
