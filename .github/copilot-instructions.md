# Copilot Instructions For docling-lab

## Core Engineering Principles

- Write clean, production-style Python with clear module boundaries.
- Prefer FastAPI for API surfaces and service endpoints.
- Use Pydantic models for request, response, and internal schema validation.
- Keep functions focused and reusable; avoid large monolithic scripts.
- Include concise comments only when logic is non-obvious.
- Include runnable, minimal README examples for new components.

## Architecture Rules

- Treat `apps/docling-serve` and `apps/label-studio` as external apps.
- Do not modify upstream behavior unless explicitly required.
- Do not mix `docling-serve` dependencies with `label-studio` dependencies.
- Every custom app/service should have its own isolated `.venv` and `pyproject.toml` where applicable.
- Custom services should call Docling Serve and Label Studio over HTTP APIs.

## Data And Artifacts

- Keep sample inputs and outputs under `data/` using small, public-safe files.
- Never commit `.venv`, `.env`, secrets, API keys, real/private documents, or large generated artifacts.
- Prefer synthetic or sanitized files for examples and demos.

## Repo Hygiene

- Keep folder structure tidy and recruiter-friendly.
- Favor explicit naming for modules, endpoints, schemas, and test data.
- Add short architecture notes when introducing new components.
- Prefer small reusable modules over one large script.
- Avoid speculative code and fake business claims.
