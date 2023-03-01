import logging
from logging import getLogger

import logstash
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    kafka_host: str = Field("kafka", env="KAFKA_HOST")
    kafka_port: int = Field(9092, env="KAFKA_PORT")
    retry_backoff_ms: int = Field(1000, env="RETRY_BACKOFF_MS")
    connections_max_idle_ms: int = Field(5000, env="CONNECTIONS_MAX_IDLE_MS")
    sentry_dsn: str = Field(
        "https://1976fd7fecf84863ad877101deebe352@o4504758500720640.ingest.sentry.io/4504758503735296", env="SENTRY_DSN"
    )
    logstash_host: str = Field("logstash", env="LOGSTASH_HOST")
    logstash_port: int = Field(5044, env="LOGSTASH_PORT")
    logstash_traces_sample_rate: float = Field(1.0, env="LOGSTASH_TRACES_SAMPLE_RATE")

    @property
    def kafka_host_port(self):
        return f"{self.kafka_host}:{self.kafka_port}"

    # We get environment variables from the docker-compose, reference to .env.


settings = Settings()
logger = getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logstash.LogstashHandler(settings.logstash_host, settings.logstash_port, version=1))
