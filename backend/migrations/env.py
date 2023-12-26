import asyncio

from alembic import context
from config import settings
from core.postgres.base import Base
from user.models import User  # noqa
from note.models import Note, Tag # noqa
from sqlalchemy.ext.asyncio import create_async_engine

config = context.config


def run_sync_migrations(connection):
    context.configure(
        connection=connection, target_metadata=Base.metadata, compare_type=True
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations(engine):
    async with engine.connect() as connection:
        await connection.run_sync(run_sync_migrations)
    await engine.dispose()


def run_migrations_online() -> None:
    engine = create_async_engine(
        settings.DATABASE_URL.unicode_string(), echo=True, future=True
    )
    asyncio.run(run_migrations(engine))


run_migrations_online()
