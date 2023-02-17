import uvicorn
import backoff
from aiokafka import AIOKafkaProducer
from fastapi import FastAPI
from kafka.errors import KafkaConnectionError

from core.config import settings
from db import kafka


app = FastAPI()


@backoff.on_exception(backoff.expo, KafkaConnectionError)
async def init_kafka() -> AIOKafkaProducer:
    aioproducer = AIOKafkaProducer(
            bootstrap_servers=[f'{settings.KAFKA_HOST}:{settings.KAFKA_PORT}'],
            retry_backoff_ms=1000,
            connections_max_idle_ms=5000
        )
    await aioproducer.start()
    return aioproducer


@app.on_event('startup')
async def startup():
    kafka.aioproducer = await init_kafka()


@app.on_event('shutdown')
async def shutdown():
    await kafka.aioproducer.stop()


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
    )
