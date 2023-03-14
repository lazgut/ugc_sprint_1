import json

import pika
from core.config import logger, rabbitmq_channel, settings
from helpers.uuid_generate import generate_uuid


def rabbitmq_publish(queue: str, author_id: str):
    rabbitmq_channel.queue_declare(queue=queue, durable=True)

    body = {
        "message_id": generate_uuid(),
        "author_id": author_id,
    }

    rabbitmq_channel.basic_publish(
        exchange="",
        routing_key=queue,
        body=json.dumps(body),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ),
    )
    logger.info(f"{body.get('message_id')} successfully publish to rabbitmq")
    return
