from typing import Optional, Self

from pydantic import PostgresDsn, RedisDsn, model_validator
from pydantic_settings import BaseSettings


class BackendSettings(BaseSettings):
    app_name: str = "Memo-Bot API"

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DATABASE: str
    POSTGRES_URL: Optional[PostgresDsn] = None

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_URL: Optional[RedisDsn] = None

    class Config:
        env_file = ".env"
        extra = "ignore"

    @model_validator(mode="before")
    def assemble_postgres_db_url(self) -> Self:
        self["POSTGRES_URL"] = PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self["POSTGRES_USER"],
            password=self["POSTGRES_PASSWORD"],
            host=self["POSTGRES_HOST"],
            port=int(self["POSTGRES_PORT"]),
            path=f'{self["POSTGRES_DATABASE"]}',
        )
        return self

    @model_validator(mode="before")
    def redis_postgres_db_url(self) -> Self:
        self["REDIS_URL"] = RedisDsn.build(scheme="redis", host=self["REDIS_HOST"], port=self["REDIS_PORT"])
        return self


settings = BackendSettings(extra="ignore")
