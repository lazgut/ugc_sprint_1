from typing import Union
import random
import uuid
from fastapi import FastAPI
from pydantic import BaseModel
from kafka import KafkaProducer

from backend.config import settings


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
    producer = KafkaProducer(bootstrap_servers=[settings.kafka_host_port])

    for i in range(20):
        # INPUT DATA
        producer.send(
            topic=view.topic,
            value=view.value,
            key=f'{view.user_uuid}+{view.movie_uuid}'.encode(),
        )

    producer.close()

