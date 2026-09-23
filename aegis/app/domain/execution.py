from enum import Enum
import uuid
from datetime import datetime, timezone

class InvalidExecutionTransition(Exception):
    pass

class ExecutionStatus(Enum):
    PENDING = "pending"
    SUCCEEDED = "succeeded"
    FAILED = "failed"

class Execution:
    def __init__(self, execution_id, status, result, error, created_at, updated_at):
        self.execution_id = execution_id
        self.status = status
        self.result = result
        self.error = error
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def create(cls):
        now = datetime.now(timezone.utc)
        return cls(
            execution_id=uuid.uuid4(),
            status=ExecutionStatus.PENDING,
            result=None,
            error=None,
            created_at=now,
            updated_at=now
        )
    def succeed(self, result):
        if self.status != ExecutionStatus.PENDING:
            raise InvalidExecutionTransition(
                f"Cannot succeed execution from status {self.status}"
            )

        if result is None:
            raise ValueError("Successful execution requires a result")
        
        self.result = result
        
        
        self.error = None
        self.status = ExecutionStatus.SUCCEEDED
        self.updated_at = datetime.now(timezone.utc)

    def fail(self, error):
        if self.status != ExecutionStatus.PENDING:
            raise InvalidExecutionTransition(
                f"Cannot fail execution from status {self.status}"
            )

        if error is None:
            raise ValueError("Failed execution requires error information")
        
        self.result = None
        self.error = error
        self.status = ExecutionStatus.FAILED
        self.updated_at = datetime.now(timezone.utc)

execution = Execution.create()

print(execution.created_at)
print(execution.updated_at)

execution.succeed("done")

print(execution.created_at)
print(execution.updated_at)
