import aioredis
from aioredis import Redis
from config import settings

redis = aioredis.from_url(settings.REDIS_URL.unicode_string(), encoding="utf-8", decode_responses=True)


async def get_session() -> Redis:
    async with redis.client() as session:
        yield session
        await session.close()
