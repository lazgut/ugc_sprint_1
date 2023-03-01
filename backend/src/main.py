import sentry_sdk
from api.v1.main import router
from core.config import settings
from db import kafka_producer
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


@app.on_event("shutdown")
async def shutdown_event():
    await kafka_producer.aioproducer.stop()


app.include_router(router, prefix="/v1")
