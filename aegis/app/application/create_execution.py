from dataclasses import dataclass
from app.domain.execution import Execution

@dataclass
class CreateExecutionCommand:
    tenant_id: str
    task: str

class CreateExecution:
    def __init__(self, repository):
        self.repository = repository

    async def create(self, command: CreateExecutionCommand):
        execution = Execution.create(
            tenant_id=command.tenant_id,
            task=command.task
        )

        self.repository.add(execution)

        return execution