from pydantic_settings import BaseSettings


class BotSettings(BaseSettings):
    TG_TOKEN: str
    TG_ADMIN: int
    TG_TOKEN_BOT_LOG: str
    TG_ADMIN_BOT_LOG: int

    class Config:
        env_file = ".env"
        extra = "ignore"


class BackendSettings(BaseSettings):
    BASE_URL: str

    class Config:
        env_file = ".env"
        extra = "ignore"


bot_settings = BotSettings(extra="ignore")
backend_settings = BackendSettings(extra="ignore")
