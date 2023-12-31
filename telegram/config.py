from pydantic_settings import BaseSettings


class BotSettings(BaseSettings):
    TG_TOKEN: str

    class Config:
        env_file = ".env"
        extra = "ignore"


class BackendSettings(BaseSettings):
    BASE_URL: str

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = BotSettings(extra="ignore")
backend_settings = BackendSettings(extra="ignore")
