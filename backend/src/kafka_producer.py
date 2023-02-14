import logging
from kafka import KafkaProducer
from config import settings

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

print("kafka server: ", settings.kafka_host_port)
logger.info(".kafka server: ", settings.kafka_host_port)

producer = KafkaProducer(bootstrap_servers=[settings.kafka_host_port], api_version=(0, 11, 5))