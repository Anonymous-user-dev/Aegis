import asyncio
from app.infra.database.base import Base
from tests.integration.conftest import test_engine

from app.infra.database import models

async def main():
    async with test_engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

asyncio.run(main())