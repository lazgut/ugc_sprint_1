import os
import logging

import pika
import requests

logger = logging.getLogger()


class Worker:
    def __init__(self):
        host_port = f'http://{os.environ["NOTIFICATOR_HOST"]}:{os.environ["NOTIFICATOR_PORT"]}'
        self.url = f'{host_port}{os.environ["ON_EVENT_URL"]}'

    def callback(self, ch, method, properties, body):
        print(" [x] Received %r" % body.decode())
        try:
            result = requests.post(self.url, data=body)
            print(result.text)
        except requests.exceptions.RequestException as e:
            logger.error(str(e))

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def main(self):
        broker_host = os.environ['BROKER_HOST']
        queue_name = os.environ['QUEUE_NAME']
        connection = pika.BlockingConnection(pika.ConnectionParameters(broker_host))
        channel = connection.channel()

        channel.queue_declare(queue=queue_name, durable=True)
        channel.basic_consume(queue=queue_name, on_message_callback=self.callback)
        # channel.basic_qos(prefetch_count=1)
        # use this ^ for balance loading between several consumers, it is not out case.

        channel.start_consuming()


if __name__ == '__main__':
    worker = Worker()
    worker.main()
