from __future__ import annotations

import json
from typing import Any

import httpx
from fastapi import FastAPI, File, Form, HTTPException, Query, UploadFile

from app.config import settings
from app.schemas import ErrorResponse, WrapperResponse

app = FastAPI(title="Docling Wrapper Service", version="0.1.0")


def _headers(tenant_id: str | None = None) -> dict[str, str]:
    headers: dict[str, str] = {}
    if settings.docling_api_key:
        headers["X-Api-Key"] = settings.docling_api_key
    chosen_tenant = tenant_id or settings.default_tenant_id
    if chosen_tenant:
        headers["X-Tenant-Id"] = chosen_tenant
    return headers


def _wrap(upstream: dict[str, Any]) -> WrapperResponse:
    status = str(upstream.get("status") or upstream.get("task_status") or "success")
    return WrapperResponse(status=status, upstream=upstream)


def _parse_options_json(options_json: str | None) -> dict[str, Any]:
    try:
        return json.loads(options_json) if options_json else {}
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=422, detail=f"Invalid options_json: {exc}") from exc


def _build_form_data(options: dict[str, Any]) -> dict[str, Any]:
    form_data: dict[str, Any] = {"target_type": "inbody"}
    for key, value in options.items():
        if value is None:
            continue
        if isinstance(value, (dict, list)):
            form_data[key] = json.dumps(value)
        elif isinstance(value, bool):
            form_data[key] = str(value).lower()
        else:
            form_data[key] = str(value)
    return form_data


async def _forward_file_request(
    endpoint_path: str,
    file: UploadFile,
    options_json: str | None,
    tenant_id: str | None,
) -> WrapperResponse:
    options = _parse_options_json(options_json)
    form_data = _build_form_data(options)

    try:
        file_bytes = await file.read()
        files = {
            "files": (file.filename or "document.bin", file_bytes, file.content_type or "application/octet-stream")
        }

        async with httpx.AsyncClient(timeout=settings.request_timeout_seconds) as client:
            response = await client.post(
                f"{settings.docling_base_url.rstrip('/')}{endpoint_path}",
                data=form_data,
                files=files,
                headers=_headers(tenant_id),
            )
            response.raise_for_status()
            return _wrap(response.json())
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=502, detail=f"Docling request failed: {exc.response.status_code}") from exc
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Docling connectivity error: {exc}") from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Unhandled wrapper error: {exc}") from exc


async def _forward_get_request(
    endpoint_path: str,
    tenant_id: str | None = None,
    params: dict[str, Any] | None = None,
) -> WrapperResponse:
    try:
        async with httpx.AsyncClient(timeout=settings.request_timeout_seconds) as client:
            response = await client.get(
                f"{settings.docling_base_url.rstrip('/')}{endpoint_path}",
                headers=_headers(tenant_id),
                params=params,
            )
            response.raise_for_status()
            return _wrap(response.json())
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=502, detail=f"Docling request failed: {exc.response.status_code}") from exc
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Docling connectivity error: {exc}") from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Unhandled wrapper error: {exc}") from exc


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post(
    "/v1/wrapper/convert/file",
    response_model=WrapperResponse,
    responses={502: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)
async def convert_file(
    file: UploadFile = File(...),
    options_json: str | None = Form(default=None),
    tenant_id: str | None = Form(default=None),
) -> WrapperResponse:
    return await _forward_file_request("/v1/convert/file", file, options_json, tenant_id)


@app.post(
    "/v1/wrapper/convert/file/async",
    response_model=WrapperResponse,
    responses={502: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)
async def convert_file_async(
    file: UploadFile = File(...),
    options_json: str | None = Form(default=None),
    tenant_id: str | None = Form(default=None),
) -> WrapperResponse:
    return await _forward_file_request("/v1/convert/file/async", file, options_json, tenant_id)


@app.get(
    "/v1/wrapper/tasks/{task_id}/status",
    response_model=WrapperResponse,
    responses={502: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)
async def get_task_status(
    task_id: str,
    wait: float = Query(default=0.0),
    tenant_id: str | None = Query(default=None),
) -> WrapperResponse:
    return await _forward_get_request(
        f"/v1/status/poll/{task_id}",
        tenant_id=tenant_id,
        params={"wait": wait},
    )


@app.get(
    "/v1/wrapper/tasks/{task_id}/result",
    response_model=WrapperResponse,
    responses={502: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)
async def get_task_result(
    task_id: str,
    tenant_id: str | None = Query(default=None),
) -> WrapperResponse:
    return await _forward_get_request(
        f"/v1/result/{task_id}",
        tenant_id=tenant_id,
    )
