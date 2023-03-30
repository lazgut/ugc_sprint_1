import logging
from typing import Optional

import backoff
from aiokafka import AIOKafkaProducer
from kafka.errors import KafkaConnectionError

from core.config import settings

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logger.info("kafka_server: ", settings.kafka_host_port)


aioproducer: Optional[AIOKafkaProducer] = None


async def get_aioproducer() -> AIOKafkaProducer:
    return aioproducer


@backoff.on_exception(backoff.expo, KafkaConnectionError)
async def init_kafka() -> AIOKafkaProducer:
    aioproducer = AIOKafkaProducer(
            bootstrap_servers=[settings.kafka_host_port],
            retry_backoff_ms=settings.RETRY_BACKOFF_MS,
            connections_max_idle_ms=settings.CONNECTIONS_MAX_IDLE_MS
        )
    await aioproducer.start()
    return aioproducer