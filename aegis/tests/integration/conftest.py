from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
import pytest_asyncio
from sqlalchemy.pool import NullPool
from app.core.config import settings

test_engine = create_async_engine(
    settings.TEST_DATABASE_URL,
    poolclass=NullPool

)

TestSessionFactory = async_sessionmaker(
    bind=test_engine,
    expire_on_commit=False
)

@pytest_asyncio.fixture
async def session():
    async with test_engine.connect() as connection:
        transaction = await connection.begin()

        Session = async_sessionmaker(
            bind=connection,
            expire_on_commit=False
        )
        async with Session() as session:
            yield session

        await transaction.rollback()