import logging
from logging import getLogger

from fastapi import FastAPI, HTTPException, Request

from db.kafka_producer import producer
from core.config import settings
from api.v1.main import router

from config import settings

logger = getLogger(__name__)
logger.setLevel(logging.INFO)

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.on_event("startup")
async def startup_event():
    print(f'kafka address: ', settings.kafka_host_port)
    # Logging doesn't work.
    kafka_producer.aioproducer = await kafka_producer.init_kafka()

@app.on_event("shutdown")
async def shutdown_event():
    await kafka_producer.aioproducer.stop()

app.include_router(router, prefix='/v1')
