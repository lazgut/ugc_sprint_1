from functools import wraps
from http import HTTPStatus

from fastapi import HTTPException
from starlette.requests import Request


def authorize(func):
    @wraps(func)
    async def inner(request: Request, **kwargs):
        user_uuid = request.headers.get("user_uuid")
        if not user_uuid:
            raise HTTPException(HTTPStatus.UNAUTHORIZED, detail="Unauthorized")
        return await func(request=request, **kwargs)
    return inner
