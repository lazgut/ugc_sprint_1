import logging
import uuid
from logging import getLogger

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from kafka import KafkaProducer

from config import settings

logger = getLogger()

app = FastAPI()


class View(BaseModel):
    user_uuid: uuid.UUID
    movie_uuid: uuid.UUID
    topic: str
    value: int


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.on_event("startup")
async def startup_event():
    print(f'kafka address: ', settings.kafka_host_port)
    # Logging doesn't work.


@app.post("/addview")
def read_item(view: View):
    """
    An example for request JSON:
    {
    "user_uuid": "d16b19e7-e116-43b1-a95d-cd5a11e8f1b4",
    "movie_uuid": "803c794c-ddf0-482d-b2c2-6fa92da4c5e2",
    "topic": "views",
    "value": 3921837
    }

    """
    producer = KafkaProducer(bootstrap_servers=[settings.kafka_host_port])
    try:
        # INPUT DATA
        print("will insert: ", view)
        producer.send(
            topic=view.topic,
            value=str(view.value).encode(),
            key=f'{view.user_uuid}+{view.movie_uuid}'.encode(),
        )
    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500, detail=str(e))
    finally:
        producer.close()

    return "OK"

