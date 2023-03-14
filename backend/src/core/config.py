import logging
from logging import getLogger

import logstash
from brokers.rabbitmq import RabbitmqConnection
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    retry_backoff_ms: int = Field(1000, env="RETRY_BACKOFF_MS")
    connections_max_idle_ms: int = Field(5000, env="CONNECTIONS_MAX_IDLE_MS")
    sentry_dsn: str = Field(
        "https://1976fd7fecf84863ad877101deebe352@o4504758500720640.ingest.sentry.io/4504758503735296",
        env="SENTRY_DSN",
    )
    logstash_host: str = Field("logstash", env="LOGSTASH_HOST")
    logstash_port: int = Field(5044, env="LOGSTASH_PORT")
    logstash_traces_sample_rate: float = Field(1.0, env="LOGSTASH_TRACES_SAMPLE_RATE")
    mongo_dsn: str = Field("localhost", env="MONGO_DSN")
    db_name: str = Field("cinema", env="DB_NAME")
    auth_host: str = Field("auth", env="AUTH_HOST")
    auth_port: int = Field(5001, env="AUTH_PORT")
    auth_secret_key: str = Field("foo", env="JWT_SECRETE_KEY")
    auth_url: str = Field("/api/v1/user/login", env="AUTH_URL")
    rabbitmq_host: str = Field("rabbitmq", env="RABBITMQ_HOST")
    rabbitmq_queue: str = Field("ugc_events", env="QUEUE_NAME")

    # We get environment variables from the docker-compose, reference to .env.

    @property
    def auth_protocol_host_port(self):
        return f"http://{self.auth_host}:{self.auth_port}"


settings = Settings()
logger = getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logstash.LogstashHandler(settings.logstash_host, settings.logstash_port, version=1, tags="backend"))

rabbitmq = RabbitmqConnection(settings.rabbitmq_host)
rabbitmq_conn = rabbitmq.init_rabbitmq_connection()
rabbitmq_channel = rabbitmq_conn.channel()
