from typing import Optional, Self

from pydantic import PostgresDsn, model_validator
from pydantic_settings import BaseSettings


class BackendSettings(BaseSettings):
    app_name: str = "Memo-Bot API"

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DATABASE: str

    DATABASE_URL: Optional[PostgresDsn] = None

    class Config:
        env_file = ".env"
        extra = "ignore"

    @model_validator(mode="before")
    def assemble_postgres_db_url(self) -> Self:
        self["DATABASE_URL"] = PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self["POSTGRES_USER"],
            password=self["POSTGRES_PASSWORD"],
            host=self["POSTGRES_HOST"],
            port=int(self["POSTGRES_PORT"]),
            path=f'{self["POSTGRES_DATABASE"]}',
        )
        return self


settings = BackendSettings(extra="ignore")
