from logging.config import dictConfig

from pydantic import BaseSettings, RedisDsn, PostgresDsn, Field


class Settings(BaseSettings):
    redis_dsn: RedisDsn
    pg_dsn: PostgresDsn
    pg_schema: str = Field("auth", env="AUTH_PG_DEFAULT_SCHEMA")
    name: str = Field("auth")
    host: str = Field("0.0.0.0", env="AUTH_HOST")
    port: int = Field(5000, env="AUTH_PORT")
    debug: bool = Field(False, env="DEBUG")
    jwt_secrete_key: str = Field("foo", env="JWT_SECRETE_KEY")
    jwt_cookie_secure: str = Field(False, env="JWT_COOKIE_SECURE")
    jwt_token_location: list = Field(["headers"], env="JWT_TOKEN_LOCATION")
    jwt_access_token_expires: int = Field(10 * 60, env="JWT_ACCESS_TOKEN_EXPIRES")
    jwt_refresh_token_expires: int = Field(
        60 * 60 * 24, env="JWT_REFRESH_TOKEN_EXPIRES"
    )
    logstash_host: str = Field("logstash", env="LOGSTASH_HOST")
    logstash_port: int = Field(5044, env="LOGSTASH_PORT")
    logstash_traces_sample_rate: float = Field(1.0, env="LOGSTASH_TRACES_SAMPLE_RATE")

    class Config:
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"

    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        }},
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi']
        }
    })


settings = Settings()
