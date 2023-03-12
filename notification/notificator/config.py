from pydantic import Field, BaseSettings


class Settings(BaseSettings):
    debug: bool = Field(False, env="DEBUG")
    email_user: str = Field("yp.group10@yandex.ru", env="EMAIL_USER")
    email_password: str = Field("notification_10", env="EMAIL_PASSWORD")


    class Config:
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
