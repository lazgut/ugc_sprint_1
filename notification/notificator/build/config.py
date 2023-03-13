from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    debug: bool = Field(False, env="DEBUG")
    email_user: str = Field("example@email.com", env="EMAIL_USER")
    email_password: str = Field("password", env="EMAIL_PASSWORD")
    postgres_host: str = Field("notificator_postgres", env="NOTIFICATION_PG_HOST")
    postgres_port: int = Field(5432, env="NOTIFICATION_PG_PORT")
    postgres_user: str = Field(env="NOTIFICATION_PG_USER")
    postgres_password:str = Field(env="NOTIFICATION_PG_PASSWORD")


settings = Settings()
