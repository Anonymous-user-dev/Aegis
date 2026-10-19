from dataclasses import dataclass
from uuid import UUID
from app.domain.execution import Execution
from app.infra.repository.execution_repository import ExecutionRepository

class ExecutionNotFound(Exception):
    pass

@dataclass
class SucceedExecutionCommand:
    execution_id: UUID
    result: str

class SucceedExecution:
    def __init__(self, repository: ExecutionRepository):
        self.repository = repository

    async def execute(self, command: SucceedExecutionCommand):
        execution = await self.repository.get_by_id(command.execution_id)

        if not execution:
            raise ExecutionNotFound(f"Execution {command.execution_id} not found")

        execution.succeed(command.result)

        await self.repository.update(execution)

        return execution
        