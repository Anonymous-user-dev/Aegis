import asyncio

from app.domain.execution import Execution
from app.infra.database.session import SessionFactory
from app.infra.repository.execution_repository import ExecutionRepository

async def main():
    execution = Execution.create()

    async with SessionFactory() as session:
        repository = ExecutionRepository(session)

        repository.add(execution)
        await session.commit()

    async with SessionFactory() as session:
        repository = ExecutionRepository(session)

        loaded = await repository.get_by_id(
            execution.execution_id
        )

        print(loaded.execution_id)
        print(loaded.status)
        print(loaded.result)

asyncio.run(main())