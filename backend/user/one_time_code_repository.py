from dataclasses import dataclass
from datetime import timedelta

from aioredis import Redis


@dataclass
class OneTimeCodeRepository:
    key_prefix: str
    period: timedelta

    def _get_key(self, user_id: int, code: int) -> str:
        return f"{self.key_prefix}_{user_id}_{code}"

    async def set(self, user_id: int, code: int, session: Redis):
        key: str = self._get_key(user_id, code)
        await session.set(key, value=1, ex=self.period)

    async def check(self, user_id: int, code: int, session: Redis) -> bool:
        key: str = self._get_key(user_id, code)
        return await session.exists(key)


auth_key_repository = OneTimeCodeRepository(key_prefix="auth_key", period=timedelta(minutes=5))
