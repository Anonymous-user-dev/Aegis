from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.domain.execution import Execution
from app.infra.database.mappers import execution_to_domain, execution_to_model
from app.infra.database.models import ExecutionModel


class ExecutionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    def add(self, execution: Execution) -> None:
        model = execution_to_model(execution=execution)
        self.session.add(model)

    async def get_by_id(self, execution_id) -> Execution | None:
        stmt = select(ExecutionModel).where(
        ExecutionModel.execution_id == execution_id
    )

        result = await self.session.execute(stmt)

        model = result.scalar_one_or_none()

        if model is None:
            return None

        return execution_to_domain(model)