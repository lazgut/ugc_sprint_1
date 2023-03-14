from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    debug: bool = Field(False, env="DEBUG")
    email_user: str = Field("example@email.com", env="EMAIL_USER")
    email_password: str = Field("password", env="EMAIL_PASSWORD")
    postgres_host: str = Field("notificator_postgres", env="NOTIFICATION_PG_HOST")
    postgres_port: int = Field(5433, env="NOTIFICATION_PG_PORT")
    postgres_user: str = Field("app", env="NOTIFICATION_PG_USER")
    postgres_password: str = Field("123qwe", env="NOTIFICATION_PG_PASSWORD")
    postgres_db_name: str = Field("notification", env="NOTIFICATION_DB_NAME")
    smtp_server: str = Field("smtp.yandex.ru", env="SMTP_SERVER")
    smtp_server_port: int = Field(465, env="SMTP_SERVER_PORT")

    pg_host: str = Field("0.0.0.0", env="PG_HOST")
    pg_port: int = Field(5432, env="PG_PORT")
    pg_user: str = Field("app", env="PG_USER")
    pg_password: str = Field("123qwe", env="PG_PASSWORD")
    pg_db_name: str = Field("movies_database", env="PG_DB_NAME")

    class Config:
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
