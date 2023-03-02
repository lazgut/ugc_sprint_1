from http import HTTPStatus

import orjson
from core.config import logger, settings
from db.mongo import get_mongo_client
from fastapi import APIRouter, HTTPException
from models.models import ReviewId, ReviewLike
from starlette.requests import Request

COLLECTION_NAME = "review_likes"
router_reviewlikes = APIRouter(prefix=f"/{COLLECTION_NAME}")


@router_reviewlikes.post("/add")
async def add_like(like: ReviewLike, request: Request):
    """
    An example request JSON:
    {
    "review_uuid": "803c794c-ddf0-482d-b2c2-6fa92da4c5e2",
    }
    We assume that request headers contain used_uuid, after processing with authentication and middleware.
    Headers:
        ...
        user_uuid: d16b19e7-e116-43b1-a95d-cd5a11e8f1b4
        ...
    """
    user_uuid = request.headers.get("user_uuid")
    if not user_uuid:
        raise HTTPException(HTTPStatus.UNAUTHORIZED, detail="Unauthorized")
    if not (0 <= like.value <= 10):
        raise HTTPException(HTTPStatus.BAD_REQUEST, "Value must be from 0 to 10.s")
    try:
        client = await get_mongo_client()
        db = client[settings.db_name]
        collection = db.get_collection(COLLECTION_NAME)
        main_idx = {
            "user": user_uuid,
            "review": str(like.review),
            "movie": str(like.movie),
        }
        result = await collection.update_one(
            main_idx, {"$set": {"value": like.value}}, upsert=True
        )

        success = True
        logger.info("Successfully added %s, user=%s, %s=%s",
                     COLLECTION_NAME, user_uuid, COLLECTION_NAME, like)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))

    return orjson.dumps({"success": success, "upserted_id": str(result.upserted_id)})


@router_reviewlikes.post("/remove")
async def remove_like(review: ReviewId, request: Request):
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
    if not user_uuid:
        raise HTTPException(401, detail="Unauthorized")
    try:
        client = await get_mongo_client()
        db = client[settings.db_name]
        collection = db.get_collection(COLLECTION_NAME)
        result = await collection.delete_one(
            {"user": user_uuid, "review": str(review.id)}
        )
        success = True
        logger.info("Successfully deleted %s, user=%s, review=%s",
                     COLLECTION_NAME, user_uuid, review)
    except Exception as e:
        logger.error("Error removing %s, user=%s, %s=%s, error=%s",
                     COLLECTION_NAME, user_uuid, COLLECTION_NAME, review, e)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))

    return orjson.dumps(
        {"success": success, "deleted_count": str(result.deleted_count)}
    )


@router_reviewlikes.get("/count")
async def count_likes(review: ReviewId, request: Request):
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
    if not user_uuid:
        raise HTTPException(401, detail="Unauthorized")
    try:
        client = await get_mongo_client()
        db = client[settings.db_name]
        collection = db.get_collection(COLLECTION_NAME)
        cursor = collection.find({"review": str(review.id)})
        values = []
        async for doc in cursor:
            values.append(doc["value"])
        average = sum(values) / len(values)
        success = True
        logger.info("Succesfully counted %s, user=%s, review=%s",
                     COLLECTION_NAME, user_uuid, review)
    except Exception as e:
        logger.error("Error counting %s, user=%s, review=%s, error=%s",
                     COLLECTION_NAME, user_uuid, review, e)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))

    return orjson.dumps({"success": success, "count": len(values), "average": average})
