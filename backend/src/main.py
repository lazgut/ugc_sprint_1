import logging
from logging import getLogger

from fastapi import FastAPI

from kafka_producer import producer
from config import settings
from api.v1.main import router

logger = getLogger(__name__)
logger.setLevel(logging.INFO)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.on_event("startup")
async def startup_event():
    print(f'kafka address: ', settings.kafka_host_port)
    # Logging doesn't work.

@app.on_event("shutdown")
async def shutdown_event():
    producer.close()

app.include_router(router, prefix='/v1')
