from http import HTTPStatus

import orjson
from core.config import logger
from fastapi import APIRouter, HTTPException
from models.models import Movie, Review
from starlette.requests import Request

from services.reviews import Reviews
from .common import check_auth

COLLECTION_NAME = "reviews"
router_reviews = APIRouter(prefix=f"/{COLLECTION_NAME}")


@router_reviews.post("/add")
async def add_review(review: Review, request: Request):
    """
    An example request JSON:
    {
    "movie": "803c794c-ddf0-482d-b2c2-6fa92da4c5e2",
    "text" : "......"
    }
    We assume that request headers contain used_uuid, after processing with authentication and middleware.
    Headers:
        ...
        user_uuid: d16b19e7-e116-43b1-a95d-cd5a11e8f1b4
        ...
    """
    user_uuid = request.headers.get("user_uuid")
    try:
        result = await Reviews.add(user_uuid, review)
        success = True
        logger.info("Successfully added %s, user=%s, %s=%s",
                     COLLECTION_NAME, user_uuid, COLLECTION_NAME, review)
    except Exception as e:
        logger.error("Error adding %s, user=%s, %s=%s, error=%s",
                     COLLECTION_NAME, user_uuid, COLLECTION_NAME, review, e)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))

    return orjson.dumps({"success": success, "inserted_id": str(result.inserted_id)})


@router_reviews.post("/remove")
async def remove_review(movie: Movie, request: Request):
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
        result = await Reviews.remove(user_uuid, movie)
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


# noinspection PyUnusedLocal
@router_reviews.get("/get")
async def get_review(movie: Movie, request: Request):
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
        review = await Reviews.get(user_uuid, movie)
        if review is None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
        success = True
        logger.info("Successfully got %s, user=%s, movie=%s",
                     COLLECTION_NAME, user_uuid, movie)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error getting %s, user=%s, movie=%s, error=%s",
                     COLLECTION_NAME, user_uuid, movie, e)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))

    return orjson.dumps(
        {"success": success, "text": review["text"], "time": review["time"]}
    )


@router_reviews.get("/list")
async def list_reviews(movie: Movie, request: Request):
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
    user_uuid = await check_auth(request)
    try:
        sort_way = request.query_params.get("sort")
        reviews_list = await Reviews.list(movie, sort_way)
        success = True
        logger.error("Successfylly listed %s, user=%s, movie=%s, sort_way=%s",
                     COLLECTION_NAME, user_uuid, movie, sort_way)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error listing %s, user=%s, movie=%s, error=%s",
                     COLLECTION_NAME, user_uuid, movie, e)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))

    return orjson.dumps({"success": success, "reviews": reviews_list})
