from pydantic import BaseSettings


class Settings(BaseSettings):
    KAFKA_DSN: str
    CLICKHOUSE_DSN: str
    CHUNK_SIZE_CH: int
    AUTO_COMMIT_CH: bool
    OFFSET_RESET_CH: str
    GROUP_ID_CH: str
    CONSUMER_TIMEOUT_MS_CH: int
    TOPIC_CH: str

    class Config:
        case_sensitive = True
        # env_file = ".env"
        # env_file_encoding = "utf-8"


settings = Settings()