# Docling Wrapper Service

FastAPI wrapper that forwards requests to Docling Serve.

## Why this service exists

- Keep your app-level API stable.
- Centralize Docling endpoint calls, headers, and error handling.
- Avoid coupling clients directly to Docling Serve request details.

## Endpoints

- `GET /health`
- `POST /v1/wrapper/convert/file`
- `POST /v1/wrapper/convert/file/async`
- `GET /v1/wrapper/tasks/{task_id}/status`
- `GET /v1/wrapper/tasks/{task_id}/result`

## Run

```bash
cd services
uv sync
source .venv/bin/activate
uv run uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

## Environment

Use `.env` in this folder if needed:

```env
DOCLING_BASE_URL=http://127.0.0.1:5001
DOCLING_API_KEY=
DEFAULT_TENANT_ID=
REQUEST_TIMEOUT_SECONDS=120
```
