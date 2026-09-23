import pytest
from app.domain.execution import Execution, ExecutionStatus, InvalidExecutionTransition

def test_create_execution():
    execution = Execution.create()

    assert execution.status == ExecutionStatus.PENDING
    assert execution.result is None
    assert execution.error is None
    assert execution.execution_id is not None
    assert execution.created_at == execution.updated_at
