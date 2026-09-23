from enum import Enum
import uuid

class InvalidExecutionTransition(Exception):
    pass

class ExecutionStatus(Enum):
    PENDING = "pending"
    SUCCEEDED = "succeeded"
    FAILED = "failed"

class Execution:
    def __init__(self, execution_id, status, result, error):
        self.execution_id = execution_id
        self.status = status
        self.result = result
        self.error = error

    @classmethod
    def create(cls):
        return cls(
            execution_id=uuid.uuid4(),
            status=ExecutionStatus.PENDING,
            result=None,
            error=None
        )
    def succeed(self, result):
        if self.status != ExecutionStatus.PENDING:
            raise InvalidExceptionTransition(
                f""
            )
        self.result = result
        self.status = ExecutionStatus.SUCCEEDED


execution = Execution.create()

print(execution.execution_id)
print(execution.status)
print(execution.result)

execution.succeed("Hello")

print(execution.status)
print(execution.result)



