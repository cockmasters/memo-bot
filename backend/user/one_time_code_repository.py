from dataclasses import dataclass
from datetime import timedelta
from typing import Optional

from redis import asyncio as aioredis


@dataclass
class OneTimeCodeRepository:
    key_prefix: str
    period: timedelta

    def _get_key(self, user_id: str, code: str) -> str:
        return f"{self.key_prefix}:{user_id}:{code}"

    async def delete(self, code: str, session: aioredis.Redis):
        pattern = self._get_key("*", code)
        keys = await session.keys(pattern)
        await session.delete(*keys)

    async def get_user_id(self, code: str, session: aioredis.Redis) -> Optional[int]:
        pattern = self._get_key("*", code)
        keys = await session.keys(pattern)
        if len(keys) == 0:
            return None
        return int(keys[0].split(":")[1])

    async def set(self, user_id: str, code: str, session: aioredis.Redis):
        key: str = self._get_key(user_id, code)
        await session.set(key, value=1, ex=self.period)

    async def check(self, user_id: str, code: str, session: aioredis.Redis) -> bool:
        key: str = self._get_key(user_id, code)
        return await session.exists(key)


auth_key_repository = OneTimeCodeRepository(key_prefix="auth_key", period=timedelta(minutes=5))
