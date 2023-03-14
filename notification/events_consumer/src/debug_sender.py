import os
import sys

import pika

broker_host = os.environ["BROKER_HOST"]
queue_name = os.environ["QUEUE_NAME"]
connection = pika.BlockingConnection(pika.ConnectionParameters(broker_host))
channel = connection.channel()

print("Send json-compatible string")
channel.queue_declare(queue=queue_name, durable=True)
message = sys.argv[1] or '{"Hello":"World!"}'
channel.basic_publish(
    exchange="",
    routing_key=queue_name,
    body=message.encode(),
    properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE),
)
print(f" [x] Sent '{message}'")
connection.close()
