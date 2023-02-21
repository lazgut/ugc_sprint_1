from pydantic import BaseSettings


class Settings(BaseSettings):
    KAFKA_HOST: str
    KAFKA_PORT: int

    @property
    def kafka_host_port(self):
        return f'{self.KAFKA_HOST}:{self.KAFKA_PORT}'

    RETRY_BACKOFF_MS: int
    CONNECTIONS_MAX_IDLE_MS: int

    SECRET: str
    ALGORITHM: str

    class Config:
        case_sensitive = True
        # Uncommented for local debug
        env_file = "C:\\Users\\artur\\PycharmProjects\\yandex_practicum\\ugc_sprint_1\\.env"
        env_file_encoding = "utf-8"


settings = Settings()
