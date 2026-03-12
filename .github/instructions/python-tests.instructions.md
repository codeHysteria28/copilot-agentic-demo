---
applyTo:
  - "**/test_*.py"
  - "**/*test*.py"
---

# Python Test Conventions

- Use **pytest** with fixtures for setup and teardown — never `unittest.TestCase`.
- Follow the **Arrange-Act-Assert** pattern: set up state, perform the action, then assert outcomes. Separate each section with a blank line.
- Use **`httpx.AsyncClient`** (via `ASGITransport`) for all API endpoint tests.
- Each test function must test **exactly one behavior**. If you need multiple assertions, they should all verify the same single behavior.
- Fixture names must **describe what they provide**, not how they work (e.g., `created_task` not `setup_task_fixture`).
- Use **`pytest.mark.parametrize`** when testing the same logic with multiple input scenarios instead of duplicating test functions.
- **Never mock what you can test directly.** Only mock external services or I/O boundaries — prefer real objects and in-memory alternatives.
