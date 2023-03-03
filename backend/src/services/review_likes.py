from typing import Tuple

from models.models import ReviewLike
from .common import Service


class ReviewLikes(Service):
    COLLECTION_NAME = "review_likes"

    @classmethod
    async def add(cls, user_uuid, like: ReviewLike):
        collection = await cls.get_collection()
        main_idx = {
            "user": user_uuid,
            "review": str(like.review),
            "movie": str(like.movie),
        }
        result = await collection.update_one(
            main_idx, {"$set": {"value": like.value}}, upsert=True
        )
        return result

    @classmethod
    async def remove(cls, user_uuid, review):
        collection = await cls.get_collection()
        result = await collection.delete_one(
            {"user": user_uuid, "review": str(review.id)}
        )
        return result

    @classmethod
    async def count(cls, review) -> Tuple[int, float]:
        """
        Returns count and average
        """
        collection = await cls.get_collection()
        cursor = collection.find({"review": str(review.id)})
        values = []
        async for doc in cursor:
            values.append(doc["value"])
        average = sum(values) / len(values)
        return len(values), average
