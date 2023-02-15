import logging
from kafka import KafkaProducer
from core.config import settings

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logger.info("kafka server: ", settings.kafka_host_port)

producer = KafkaProducer(bootstrap_servers=[settings.kafka_host_port], api_version=(0, 11, 5))