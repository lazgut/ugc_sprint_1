import logging
from typing import Optional

import backoff
from aiokafka import AIOKafkaProducer
from kafka.errors import KafkaConnectionError

from core.config import settings

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logger.info("kafka server: ", settings.kafka_host_port)

producer = AIOKafkaProducer(bootstrap_servers=[settings.kafka_host_port])



aioproducer: Optional[AIOKafkaProducer] = None


async def get_aioproducer() -> AIOKafkaProducer:
    return aioproducer


@backoff.on_exception(backoff.expo, KafkaConnectionError)
async def init_kafka() -> AIOKafkaProducer:
    aioproducer = AIOKafkaProducer(
            bootstrap_servers=[settings.kafka_host_port],
            retry_backoff_ms=1000,
            connections_max_idle_ms=5000
        )
    await aioproducer.start()
    return aioproducer
