import json
import logging

import pika

from brokers.rabbitmq import RabbitmqConnection
from core.config import settings
from helpers.uuid_generate import generate_uuid

logger = logging.getLogger(__name__)


def rabbitmq_publish(queue: str, author_id: str):
    rabbitmq = RabbitmqConnection(settings.rabbitmq_host)
    rabbitmq_conn = rabbitmq.init_rabbitmq_connection()
    rabbitmq_channel = rabbitmq_conn.channel()

    rabbitmq_channel.queue_declare(queue=queue, durable=True)

    body = {
        "message_id": generate_uuid(),
        "author_id": author_id,
    }

    logger.info(f"RABBITMQ body: {body}")
    rabbitmq_channel.basic_publish(
        exchange="",
        routing_key=queue,
        body=json.dumps(body),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ),
    )
    rabbitmq_conn.close()

    logger.info(f"{body.get('message_id')} successfully publish to rabbitmq")
    return
