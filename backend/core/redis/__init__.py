from config import settings
from redis import asyncio as aioredis

redis = aioredis.from_url(settings.REDIS_URL.unicode_string(), encoding="utf-8", decode_responses=True)


async def get_session() -> aioredis.Redis:
    async with redis.client() as session:
        yield session
        await session.close()
