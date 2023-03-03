import datetime
from http import HTTPStatus

import orjson
from core.config import logger, settings
from db.mongo import get_mongo_client
from fastapi import APIRouter, HTTPException
from models.models import Bookmark, Movie
from starlette.requests import Request

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
        client = await get_mongo_client()
        db = client[settings.db_name]
        collection = db.get_collection(COLLECTION_NAME)
        result = await collection.insert_one(
            {
                "user": user_uuid,
                "movie": str(bookmark.movie),
                "time": datetime.datetime.now(),
            }
        )
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
        client = await get_mongo_client()
        db = client[settings.db_name]
        collection = db.get_collection(COLLECTION_NAME)
        result = await collection.delete_one(
            {"user": user_uuid, "movie": str(bookmark.movie)}
        )
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
        client = await get_mongo_client()
        db = client[settings.db_name]
        collection = db.get_collection(COLLECTION_NAME)

        objects = collection.find({"movie": str(movie.id)}).sort("time", 1)
        objects_list = [
            {
                "user": r["user"],
                "movie": r["movie"],
                "id": str(r["_id"]),
                "time": str(r["time"]),
            }
            async for r in objects
        ]

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
