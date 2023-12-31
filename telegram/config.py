from pydantic_settings import BaseSettings


class BotSettings(BaseSettings):
    BOT_TOKEN: str

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = BotSettings(extra="ignore")
