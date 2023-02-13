import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    kafka_host: str = os.environ['KAFKA_HOST']
    kafka_port: int = os.environ['KAFKA_PORT']

    @property
    def kafka_host_port(self):
        return f'{self.kafka_host}:{self.kafka_port}'

    class Config:
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()