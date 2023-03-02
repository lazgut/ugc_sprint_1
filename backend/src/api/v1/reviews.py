import datetime
from http import HTTPStatus

import orjson
from core.config import logger, settings
from db.mongo import get_mongo_client
from fastapi import APIRouter, HTTPException
from models.models import Movie, Review
from starlette.requests import Request

COLLECTION_NAME = "reviews"
router_reviews = APIRouter(prefix=f"/{COLLECTION_NAME}")


@router_reviews.post("/add")
async def add_review(review: Review, request: Request):
    """
    An example request JSON:
    {
    "movie_uuid": "803c794c-ddf0-482d-b2c2-6fa92da4c5e2",
    "text" : "......"
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
    try:
        client = await get_mongo_client()
        db = client[settings.db_name]
        collection = db.get_collection(COLLECTION_NAME)
        result = await collection.insert_one(
            {
                "user": user_uuid,
                "movie": str(review.movie),
                "text": review.text,
                "time": datetime.datetime.now(),
            }
        )
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
    user_uuid = request.headers.get("user_uuid")
    if not user_uuid:
        raise HTTPException(401, detail="Unauthorized")
    try:
        client = await get_mongo_client()
        db = client[settings.db_name]
        collection = db.get_collection(COLLECTION_NAME)
        result = await collection.delete_one(
            {"user": user_uuid, "movie": str(movie.id)}
        )
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
    user_uuid = request.headers.get("user_uuid")
    if not user_uuid:
        raise HTTPException(401, detail="Unauthorized")
    try:
        client = await get_mongo_client()
        db = client[settings.db_name]
        collection = db.get_collection(COLLECTION_NAME)
        review = await collection.find_one({"movie": str(movie.id), "user": user_uuid})
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
    user_uuid = request.headers.get("user_uuid")
    if not user_uuid:
        raise HTTPException(401, detail="Unauthorized")
    try:
        client = await get_mongo_client()
        db = client[settings.db_name]
        collection = db.get_collection(COLLECTION_NAME)  # reviews
        sort_way = request.query_params.get("sort")

        reviews = collection.find({"movie": str(movie.id)})
        reviews_list = [
            {
                "user": r["user"],
                "movie": r["movie"],
                "id": str(r["_id"]),
                "text": r["text"],
                "time": str(r["time"]),
            }
            async for r in reviews
        ]
        if sort_way is not None:
            review_likes_collection = db.get_collection("review_likes")
            review_likes_query = review_likes_collection.aggregate(
                [
                    {"$match": {"movie": str(movie.id)}},
                    {
                        "$group": {
                            "_id": "$review",
                            "count": {"$count": {}},
                            "average": {"$avg": "$value"},
                        }
                    },
                ]
            )
            reviews_rate = {}
            review_likes_list = await review_likes_query.to_list(length=None)
            # async for doesn't work.
            # async for review_line in review_likes_query:
            #    reviews_rate[str(review_line['_id'])] = (review_line['count'], review_line['average'])
            reviews_rate = {
                str(rl["_id"]): (rl["count"], rl["average"]) for rl in review_likes_list
            }
            if len(reviews_list):
                if sort_way == "likes_count":
                    reviews_list.sort(key=lambda r: reviews_rate[r["id"]][0])
                elif sort_way == "average_rate":
                    reviews_list.sort(key=lambda r: reviews_rate[r["id"]][1])
                else:
                    raise HTTPException(
                        status_code=HTTPStatus.NOT_ACCEPTABLE,
                        detail="Unsupported sorting method",
                    )

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
