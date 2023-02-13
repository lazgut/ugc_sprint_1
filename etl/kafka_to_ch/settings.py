from pydantic import AnyUrl, BaseSettings, Field


class Settings(BaseSettings):
    kafka_dsn: str = Field("localhost:9092", env="KAFKA_DSN")  # библиотека Kafka сплитит порт через ':', поэтому str
    clickhouse_dsn: str = Field("clickhouse://localhost", env="CLICKHOUSE_DSN")
    chunk_size_ch: int = Field(10000, env="CHUNK_SIZE_CH")
    auto_commit_ch: bool = Field(False, env="AUTO_COMMIT_CH")
    offset_reset_ch: str = Field("earliest", env="OFFSET_RESET_CH")
    group_id_ch: str = Field("echo-messages-to-stdout", env="GROUP_ID_CH")
    consumer_timeout_ms_ch: int = Field(1000, env="CONSUMER_TIMEOUT_MS_CH")
    topic_ch: str = Field("views", env="TOPIC_CH")

    class Config:
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"
