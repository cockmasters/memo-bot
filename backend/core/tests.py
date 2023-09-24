from backend.config import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import scoped_session, sessionmaker

test_engine = create_async_engine(
    settings.DATABASE_URL.unicode_string(), echo=True, future=True
)
test_async_session_maker = sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)
test_session = scoped_session(test_async_session_maker)
