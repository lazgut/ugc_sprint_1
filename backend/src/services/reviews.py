import datetime
from typing import Literal, Optional

from models.models import Movie, Review
from services.common import Service


class Reviews(Service):
    COLLECTION_NAME = "reviews"

    @classmethod
    async def add(cls, user_uuid, review: Review):
        collection = await cls.get_collection()
        result = await collection.insert_one(
            {
                "user": user_uuid,
                "movie": str(review.movie),
                "text": review.text,
                "time": datetime.datetime.now(),
            }
        )
        return result

    @classmethod
    async def remove(cls, user_uuid, movie: Movie):
        collection = await cls.get_collection()
        result = await collection.delete_one(
            {"user": user_uuid, "movie": str(movie.id)}
        )
        return result

    @classmethod
    async def get(cls, user_uuid, movie: Movie):
        collection = await cls.get_collection()
        review = await collection.find_one({"movie": str(movie.id), "user": user_uuid})
        return review

    @classmethod
    async def list(cls, movie: Movie,
                   sort_way: Optional[Literal["likes_count", "average_rate"]]) -> list[dict]:
        """
        Can raise ValueError.
        Returns review list sorted.
        """
        collection = await cls.get_collection()
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
            review_likes_collection = await cls.get_collection("review_likes")
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
                    raise ValueError("Unsupported sorting method")
        return reviews_list