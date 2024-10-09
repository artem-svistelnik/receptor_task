from fastapi import HTTPException, status
from starlette.requests import Request
from starlette.responses import JSONResponse


class ApiError(Exception):
    status_code: int = status.HTTP_404_NOT_FOUND
    detail: str = "Not found"

    def __init__(self, detail: str = None, status_code: int = None):
        self.detail = detail or self.detail
        self.status_code = status_code or self.status_code

    def __str__(self):
        return f"{self.status_code}: {self.detail}"


async def api_error_handler(request: Request, exc: ApiError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

