import os
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    kafka_host: str = Field('kafka', env='KAFKA_HOST')
    kafka_port: int = Field(9092, env='KAFKA_PORT')
    retry_backoff_ms: int = Field(1000, env='RETRY_BACKOFF_MS')
    connections_max_idle_ms: int = Field(5000, env='CONNECTIONS_MAX_IDLE_MS')

    @property
    def kafka_host_port(self):
        return f'{self.kafka_host}:{self.kafka_port}'

    # We get environment variables from the docker-compose, reference to .env.

settings = Settings()