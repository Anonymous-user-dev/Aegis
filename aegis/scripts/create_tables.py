import asyncio
from app.infra.database.base import Base
from app.infra.database.session import engine

from app.infra.database import models

async def main():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

asyncio.run(main())