import pytest_asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.pool import NullPool
from app.core.config import settings
from collections.abc import AsyncIterator
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.api.dependencies import get_session

test_engine = create_async_engine(
    settings.TEST_DATABASE_URL,
    poolclass=NullPool

)

TestSessionFactory = async_sessionmaker(
    bind=test_engine,
    expire_on_commit=False

)

async def get_test_session() -> AsyncIterator[AsyncSession]:
    async with TestSessionFactory() as session:
        yield session
    
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


@pytest_asyncio.fixture
async def client(session):
    async def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        yield client

    app.dependency_overrides.clear()