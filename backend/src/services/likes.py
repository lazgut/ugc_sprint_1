from typing import Tuple

from models.models import Like, Movie

from .common import Service


class Likes(Service):
    COLLECTION_NAME = "likes"

    @classmethod
    async def add(cls, user_uuid, like: Like):
        collection = await cls.get_collection()
        main_idx = {"user": user_uuid, "movie": str(like.movie)}
        result = await collection.update_one(main_idx, {"$set": {"value": like.value}}, upsert=True)
        return result

    @classmethod
    async def remove(cls, user_uuid, movie):
        collection = await cls.get_collection()
        result = await collection.delete_one({"user": user_uuid, "movie": str(movie.id)})
        return result

    @classmethod
    async def count(cls, movie: Movie) -> Tuple[int, float]:
        """
        Returns count and average value
        """
        collection = await cls.get_collection()
        cursor = collection.find({"movie": str(movie.id)})
        values = []
        async for doc in cursor:
            values.append(doc["value"])
        average = sum(values) / len(values)
        return len(values), average
