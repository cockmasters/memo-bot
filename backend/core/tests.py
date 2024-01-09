from config import settings
from redis import asyncio as aioredis
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import scoped_session, sessionmaker

test_postgres_engine = create_async_engine(settings.POSTGRES_URL.unicode_string(), echo=True, future=True)
test_async_session_maker = sessionmaker(
    test_postgres_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)
test_session = scoped_session(test_async_session_maker)


test_redis = aioredis.from_url(settings.REDIS_URL.unicode_string(), encoding="utf-8", decode_responses=True)
