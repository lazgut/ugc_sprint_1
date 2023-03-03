from http import HTTPStatus

import orjson
from core.config import logger
from fastapi import APIRouter, HTTPException
from models.models import Bookmark, Movie
from starlette.requests import Request

from services.bookmarks import Bookmarks
from .common import authorize


COLLECTION_NAME = "bookmarks"
router_bookmarks = APIRouter(prefix=f"/{COLLECTION_NAME}")


@router_bookmarks.post("/add")
@authorize
async def add_bookmark(bookmark: Bookmark, request: Request):
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
    user_uuid = request.headers.get("user_uuid")
    try:
        result = await Bookmarks.add(user_uuid, bookmark)
        success = True
        logger.info("Successfully added %s, user=%s, %s=%s",
                     COLLECTION_NAME, user_uuid, COLLECTION_NAME, bookmark)
    except Exception as e:
        logger.error("Error adding %s, user=%s, %s=%s, error=%s",
                     COLLECTION_NAME, user_uuid, COLLECTION_NAME, bookmark, e)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))

    return orjson.dumps({"success": success, "inserted_id": str(result.inserted_id)})


@router_bookmarks.post("/remove")
@authorize
async def remove_bookmark(bookmark: Bookmark, request: Request):
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
    user_uuid = request.headers.get("user_uuid")
    try:
        result = await Bookmarks.remove(user_uuid, bookmark)
        success = True
        logger.info("Successfully removed %s, user=%s, %s=%s",
                     COLLECTION_NAME, user_uuid, COLLECTION_NAME, bookmark)
    except Exception as e:
        logger.error("Error removing %s, user=%s, %s=%s, error=%s",
                     COLLECTION_NAME, user_uuid, COLLECTION_NAME, bookmark, e)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))

    return orjson.dumps(
        {"success": success, "deleted_count": str(result.deleted_count)}
    )


@router_bookmarks.get("/list")
@authorize
async def list_bookmarks(movie: Movie, request: Request):
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
    + Optional request parameter
        sort: likes_count | average_rate
    """
    # TODO Make pagination.
    user_uuid = request.headers.get("user_uuid")
    try:
        objects_list = await Bookmarks.list(movie)

        success = True
        logger.info("Successfully listed %s, user=%s, movie=%s",
                     COLLECTION_NAME, user_uuid, movie)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error listing %s, user=%s, movie=%s, error=%s",
                     COLLECTION_NAME, user_uuid, movie, e)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))

    return orjson.dumps({"success": success, COLLECTION_NAME: objects_list})
