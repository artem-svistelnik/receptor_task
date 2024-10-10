from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class SecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        body = await request.body()

        if b"import os" in body or b"eval" in body or b"exec" in body:
            return Response(content="Unsupported Syntax", status_code=400)

        response = await call_next(request)
        return response
