import uvicorn
import backoff
from aiokafka import AIOKafkaProducer
from fastapi import FastAPI
from kafka.errors import KafkaConnectionError

from core.config import settings
from db import kafka_producer
from api.v1.api import router

app = FastAPI()


@backoff.on_exception(backoff.expo, KafkaConnectionError)
async def init_kafka() -> AIOKafkaProducer:
    aioproducer = AIOKafkaProducer(
            bootstrap_servers=[f'{settings.KAFKA_HOST}:{settings.KAFKA_PORT}'],
            retry_backoff_ms=settings.RETRY_BACKOFF_MS,
            connections_max_idle_ms=settings.CONNECTIONS_MAX_IDLE_MS
        )
    await aioproducer.start()
    return aioproducer


@app.on_event('startup')
async def startup():
    kafka_producer.aioproducer = await init_kafka()


@app.on_event('shutdown')
async def shutdown():
    await kafka_producer.aioproducer.stop()


app.include_router(router, prefix='/v1')


# if __name__ == '__main__':
#     uvicorn.run(
#         'main:app',
#         host='0.0.0.0',
#         port=8000,
#         reload=True,
#     )
