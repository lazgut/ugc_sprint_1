import logging
from typing import Union
import random
import uuid
from logging import getLogger

from fastapi import FastAPI
from pydantic import BaseModel
from kafka import KafkaProducer

from backend.config import settings

logger = getLogger()
logger.setLevel(logging.INFO)

app = FastAPI()


class View(BaseModel):
    user_uuid: uuid.UUID
    movie_uuid: uuid.UUID
    topic: str
    value: int


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/addview")
def read_item(view: View):
    # return {"item_id": item_id, "q": q}
    logger.info('kafka address: %s', settings.kafka_host_port)
    print(f'kafka address: ', settings.kafka_host_port)
    producer = KafkaProducer(bootstrap_servers=[settings.kafka_host_port])

    for i in range(20):
        # INPUT DATA
        print("will insert: ", view)
        producer.send(
            topic=view.topic,
            value=str(view.value).encode(),
            key=f'{view.user_uuid}+{view.movie_uuid}'.encode(),
        )

    producer.close()
    return "OK"

