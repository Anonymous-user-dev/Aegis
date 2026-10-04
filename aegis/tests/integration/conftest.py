from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from sqlalchemy.pool import NullPool
from app.core.config import settings

test_engine = create_async_engine(
    settings.DATABASE_URL,
    poolclass=NullPool

)

TestSessionFactory = async_sessionmaker(
    bind=test_engine,
    expire_on_commit=False
)
