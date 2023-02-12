from pydantic import BaseSettings, KafkaDsn


class Settings(BaseSettings):
    # kafka_dsn: KafkaDsn
    # clickhouse_host: str
    # clickhouse_port: str

    class Config:
        case_sensitive = False
        env_file = '.env'
        env_file_encoding = 'utf-8'
