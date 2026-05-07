from pydantic import BaseModel


class WrapperResponse(BaseModel):
    status: str
    upstream: dict[str, Any]


class ErrorResponse(BaseModel):
    detail: str
