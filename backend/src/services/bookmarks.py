import datetime

from models.models import Bookmark
from .common import Service


class Bookmarks(Service):
    COLLECTION_NAME = "bookmarks"

    @classmethod
    async def add(cls, user_uuid, bookmark: Bookmark):
        collection = await cls.get_collection()
        result = await collection.insert_one(
            {
                "user": user_uuid,
                "movie": str(bookmark.movie),
                "time": datetime.datetime.now(),
            }
        )
        return result


    @classmethod
    async def remove(cls, user_uuid, bookmark: Bookmark):
        collection = await cls.get_collection()
        result = await collection.delete_one(
            {"user": user_uuid, "movie": str(bookmark.movie)}
        )
        return result

    @classmethod
    async def list(cls, movie):
        collection = await cls.get_collection()
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
        return objects_list