from pydantic import BaseSettings


class Settings(BaseSettings):
    TOPIC_CH: str
    KAFKA_DSN: str
    CLICKHOUSE_DSN: str
    CHUNK_SIZE_CH: int
    AUTO_COMMIT_CH: bool
    OFFSET_RESET_CH: str
    GROUP_ID_CH: str
    CONSUMER_TIMEOUT_MS_CH: int

    class Config:
        case_sensitive = True
