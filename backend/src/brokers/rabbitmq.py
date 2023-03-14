import pika
from pika import BlockingConnection


class RabbitmqConnection:
    def __init__(self, host):
        self.host = host

    def init_rabbitmq_connection(self) -> BlockingConnection:
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
        return connection
