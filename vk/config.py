from pydantic import BaseSettings


class BotSettings(BaseSettings):
    GROUP_TOKEN: str


settings = BotSettings()
