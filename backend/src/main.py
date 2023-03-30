import logging
from logging import getLogger
import uvicorn

from fastapi import FastAPI

from db import kafka_producer
from api.v1.api import router


logger = getLogger(__name__)
logger.setLevel(logging.INFO)

app = FastAPI()


@app.on_event('startup')
async def startup():
    kafka_producer.aioproducer = await kafka_producer.init_kafka()


@app.on_event('shutdown')
async def shutdown():
    await kafka_producer.aioproducer.stop()


app.include_router(router, prefix='/v1')


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)