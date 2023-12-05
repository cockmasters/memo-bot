from backend.config import settings
from backend.core.postgres.base import Base
from sqlalchemy.ext.asyncio import async_sessionmaker  # noqa
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine  # noqa

engine = create_async_engine(
    settings.DATABASE_URL.unicode_string(), echo=True, future=True
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()


async def get_session() -> AsyncSession:
    async_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
        await session.commit()
        await session.close()
