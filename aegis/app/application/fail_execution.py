from uuid import UUID
from dataclasses import dataclass
from app.infra.repository.execution_repository import ExecutionRepository
from app.domain.execution import Execution

class ExecutionNotFound(Exception):
    pass

@dataclass
class ExecutionFailCommand:
    execution_id: UUID
    error: str


class ExecutionFail:
    def __init__(self, repository: ExecutionRepository):
        self.repository = repository

    async def execute(self, command: ExecutionFailCommand) -> Execution:
        execution = await self.repository.get_by_id(command.execution_id)

        if not execution:
            raise ExecutionNotFound(f"Execution {command.execution_id} not found")

        execution.fail(command.error)

        await self.repository.update(execution)

        return execution

    