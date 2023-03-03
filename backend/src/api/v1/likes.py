from http import HTTPStatus

import orjson
from core.config import logger
from fastapi import APIRouter, HTTPException
from models.models import Like, Movie
from starlette.requests import Request

from services.likes import Likes
from .common import check_auth


COLLECTION_NAME = "likes"
router_likes = APIRouter(prefix=f"/{COLLECTION_NAME}")


@router_likes.post("/add")
async def add_like(like: Like, request: Request):
    """
    An example request JSON:
    {
    "movie_uuid": "803c794c-ddf0-482d-b2c2-6fa92da4c5e2",
    }
    We assume that request headers contain used_uuid, after processing with authentication and middleware.
    Headers:
        ...
        user_uuid: d16b19e7-e116-43b1-a95d-cd5a11e8f1b4
        ...
    """
    if not (0 <= like.value <= 10):
        raise HTTPException(HTTPStatus.BAD_REQUEST, "Value must be from 0 to 10.s")
    user_uuid = await check_auth(request)
    try:
        result = await Likes.add(user_uuid, like)

        success = True
        logger.info("Successfully added %s, user=%s, %s=%s",
                     COLLECTION_NAME, user_uuid, COLLECTION_NAME, like)
    except Exception as e:
        logger.error("Error adding %s, user=%s, %s=%s, error=%s",
                     COLLECTION_NAME, user_uuid, COLLECTION_NAME, like, e)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))

    return orjson.dumps({"success": success, "upserted_id": str(result.upserted_id)})


@router_likes.post("/remove")
async def remove_like(movie: Movie, request: Request):
    """
    An example request JSON:
    {
    "id": "803c794c-ddf0-482d-b2c2-6fa92da4c5e2",
    }
    We assume that request headers contain used_uuid, after processing with authentication and middleware.
    Headers:
        ...
        user_uuid: d16b19e7-e116-43b1-a95d-cd5a11e8f1b4
        ...
    """
    user_uuid = await check_auth(request)
    try:
        result = await Likes.remove(user_uuid, movie)
        success = True
        logger.info("Successfully deleted %s, user=%s, movie=%s",
                     COLLECTION_NAME, user_uuid, movie)
    except Exception as e:
        logger.error("Error removing %s, user=%s, movie=%s, error=%s",
                     COLLECTION_NAME, user_uuid, movie, e)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))

    return orjson.dumps(
        {"success": success, "deleted_count": str(result.deleted_count)}
    )


@router_likes.get("/count")
async def count_likes(movie: Movie, request: Request):
    """
    An example request JSON:
    {
    "id": "803c794c-ddf0-482d-b2c2-6fa92da4c5e2",
    }
    We assume that request headers contain used_uuid, after processing with authentication and middleware.
    Headers:
        ...
        user_uuid: d16b19e7-e116-43b1-a95d-cd5a11e8f1b4
        ...
    """
    user_uuid = await check_auth(request)
    try:
        count, average = await Likes.count(movie)
        success = True
        logger.info("Successfully counted %s, user=%s, movie=%s",
                     COLLECTION_NAME, user_uuid, movie)
    except Exception as e:
        logger.error("Error getting %s, user=%s, movie=%s, error=%s",
                     COLLECTION_NAME, user_uuid, movie, e)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))

    return orjson.dumps({"success": success, "count": count, "average": average})
