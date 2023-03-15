import logging

import sentry_sdk
import uvicorn

from api.v1.bookmarks import router_bookmarks
from api.v1.likes import router_likes
from api.v1.main import router
from api.v1.review_likes import router_reviewlikes
from api.v1.reviews import router_reviews
from core.config import settings
from core.logger import LOGGING
from db import mongo
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.on_event("startup")
async def startup_event():
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=settings.logstash_traces_sample_rate,
    )

    # Logging doesn't work.
    # kafka_producer.aioproducer = await kafka_producer.init_kafka()
    mongo.mongo_client = await mongo.init_mongo_client()


@app.on_event("shutdown")
async def shutdown_event():
    mongo.mongo_client.close()


V1 = "/v1"
app.include_router(router, prefix=V1)
app.include_router(router_likes, prefix=V1)
app.include_router(router_reviews, prefix=V1)
app.include_router(router_reviewlikes, prefix=V1)
app.include_router(router_bookmarks, prefix=V1)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_config=LOGGING,
                log_level=logging.DEBUG)
