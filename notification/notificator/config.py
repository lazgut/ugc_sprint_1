from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    debug: bool = Field(False, env="DEBUG")
    email_user: str = Field("example@email.com", env="EMAIL_USER")
    email_password: str = Field("password", env="EMAIL_PASSWORD")

    class Config:
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
