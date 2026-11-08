from typing import Any

from pydantic import BaseModel


class BaseResponse(BaseModel):
    code: int
    message: str
    data: Any | None = None


class SuccessResponse(BaseResponse):
    code: int = 0
    message: str = "SUCCESS"


class ErrorResponse(BaseResponse):
    code: int = 1000
    message: str = "ERROR"
