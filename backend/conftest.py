import asyncio

import pytest
import pytest_asyncio
from app import app as client_app
from core.postgres import Base
from core.tests import test_postgres_engine, test_redis
from httpx import AsyncClient
from redis import asyncio as aioredis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from user.note.tests.factories import NoteFactory


@pytest.yield_fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def prepare_db(
    event_loop,
):  # TODO: Исправить, чтобы схема не накатывалась на каждом тесте
    async with test_postgres_engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
        await connection.commit()


@pytest_asyncio.fixture
async def async_session(prepare_db) -> AsyncSession:
    async_session = async_sessionmaker(test_postgres_engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
        await session.commit()
        await session.close()


@pytest_asyncio.fixture
async def aioredis_session() -> aioredis.Redis:
    async with test_redis.client() as session:
        yield session
        await session.close()


@pytest_asyncio.fixture(autouse=True)
async def aioredis_prepare_db(aioredis_session):
    await aioredis_session.flushdb()


@pytest.fixture
def client() -> AsyncClient:
    yield AsyncClient(app=client_app, base_url="http://test")


@pytest.fixture
def note_factory():
    return lambda *args, **kwargs: NoteFactory(*args, **kwargs)
