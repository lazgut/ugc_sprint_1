from typing import Optional

import motor.motor_asyncio
import pymongo
from core.config import logger, settings


mongo_client: Optional[motor.motor_asyncio.AsyncIOMotorClient] = None


async def get_mongo_client():
    return mongo_client


async def init_mongo_client():
    conn_str = settings.mongo_dsn
    # set a 5-second connection timeout
    mongo_client = motor.motor_asyncio.AsyncIOMotorClient(
        conn_str, serverSelectionTimeoutMS=5000, uuidRepresentation="standard"
    )
    # Just to check the connection:
    logger.info(await mongo_client.server_info())
    await create_indices(mongo_client)
    return mongo_client


async def create_indices(_mongo_client: motor.motor_asyncio.AsyncIOMotorClient):
    db: motor.motor_asyncio.AsyncIOMotorDatabase = _mongo_client[settings.db_name]
    collections = await db.list_collection_names()

    async def make_indexes(collection_name, field2):
        if collection_name in collections:
            collection = db.get_collection(collection_name)
        else:
            collection: motor.MotorCollection = await db.create_collection(
                collection_name
            )

        await collection.create_index(
            [("user", pymongo.ASCENDING), (field2, pymongo.ASCENDING)], unique=True
        )
        await collection.create_index(field2)
        return collection

    await make_indexes("likes", "movie")
    await make_indexes("reviews", "movie")
    review_likes = await make_indexes("review_likes", "review")
    # Additional: movie to review_like:
    await review_likes.create_index(
        [
            ("movie", pymongo.ASCENDING),
            ("user", pymongo.ASCENDING),
            ("review", pymongo.ASCENDING),
        ],
        unique=True,
    )

    await make_indexes("bookmarks", "movie")
