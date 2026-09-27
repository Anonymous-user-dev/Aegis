from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.execution import Execution
from app.infra.database.mappers import execution_to_domain, execution_to_model
from app.infra.database.models import ExecutionModel

class ExecutionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, execution: Execution) -> None:
        model = execution_to_model(execution=execution)
        self.session.add(model)