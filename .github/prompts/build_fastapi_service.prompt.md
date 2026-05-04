# Build FastAPI Service Prompt

Build a production-style FastAPI service in this repository with clean modular Python structure.

## Requirements

- Use Python, FastAPI, Pydantic, and uv.
- Organize code into small reusable modules.
- Include a health check endpoint (`GET /health`).
- Add configuration module for environment-driven settings.
- Define request/response schemas with Pydantic models.
- Create route modules and service-layer modules.
- Add tests for health and at least one business endpoint.
- Include concise README run/test examples.

## Constraints

- Keep service dependencies isolated in its own project folder.
- Do not mix dependencies with `apps/docling-serve` or `apps/label-studio`.
- Keep examples generic and public-safe.

## Deliverables

- `pyproject.toml`
- FastAPI app entrypoint
- `schemas`, `routers`, `services`, `core` modules
- basic tests
- README snippet with `uv sync`, run, and test commands
