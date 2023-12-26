import asyncio

import pytest
import pytest_asyncio
from app import app as client_app
from core.postgres import Base
from core.tests import test_engine
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


@pytest.yield_fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def prepare_db(
    event_loop,
):  # TODO: Исправить, чтобы схема не накатывалась на каждом тесте
    async with test_engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
        await connection.commit()


@pytest_asyncio.fixture
async def async_session(prepare_db) -> AsyncSession:
    async_session = async_sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
        await session.commit()
        await session.close()


@pytest.fixture
def client() -> AsyncClient:
    yield AsyncClient(app=client_app, base_url="http://test")
