from pydantic import BaseSettings


class BotSettings(BaseSettings):
    VK_GROUP_TOKEN: str
    BASE_URL: str


settings = BotSettings()
