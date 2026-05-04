from typing import Any

from pydantic import BaseModel, ConfigDict, HttpUrl


class ConvertFromUrlRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_url: HttpUrl
    tenant_id: str | None = None
    options: dict[str, Any] = {}


class WrapperResponse(BaseModel):
    status: str
    upstream: dict[str, Any]


class ErrorResponse(BaseModel):
    detail: str
