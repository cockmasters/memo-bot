from pydantic_settings import BaseSettings


class BotSettings(BaseSettings):
    SERVER_PORT: int = 8000
    SERVER_HOST: str = "127.0.0.1"

    BOT_TOKEN: str

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = BotSettings(extra="ignore")
