import json
import logging
import os

import pika
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Worker:
    def __init__(self):
        # TODO delete this comment
        # os.environ["NOTIFICATOR_HOST"] = '0.0.0.0'
        # os.environ["NOTIFICATOR_PORT"] = '5000'
        # os.environ["ON_EVENT_URL"] = 'v1/manual_sender'
        # os.environ['BROKER_HOST'] = '0.0.0.0'
        # os.environ['QUEUE_NAME'] = 'ugc_events'

        host_port = f'http://{os.environ["NOTIFICATOR_HOST"]}:{os.environ["NOTIFICATOR_PORT"]}'
        self.url = f'{host_port}{os.environ["ON_EVENT_URL"]}'

    def callback(self, ch, method, properties, body):
        try:
            result = requests.post(self.url, json=json.loads(body), headers={"Content-Type": "application/json"})
            ch.basic_ack(delivery_tag=method.delivery_tag)
            logger.info(result.text)
        except requests.exceptions.RequestException as e:
            logger.error(str(e))

    def main(self):
        broker_host = os.environ["BROKER_HOST"]
        logger.info("Connecting to %s", broker_host)
        queue_name = os.environ["QUEUE_NAME"]
        connection = pika.BlockingConnection(pika.ConnectionParameters(broker_host))
        channel = connection.channel()

        channel.queue_declare(queue=queue_name, durable=True)
        channel.basic_consume(queue=queue_name, on_message_callback=self.callback, auto_ack=False)
        channel.basic_qos(prefetch_count=1)
        logger.info(f"Starting, url:{self.url}")
        channel.start_consuming()


if __name__ == "__main__":
    worker = Worker()
    worker.main()
