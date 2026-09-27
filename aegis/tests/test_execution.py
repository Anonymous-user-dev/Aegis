import pytest
from app.domain.execution import Execution, ExecutionStatus, InvalidExecutionTransition

def test_create_execution():
    execution = Execution.create()

    assert execution.status == ExecutionStatus.PENDING
    assert execution.result is None
    assert execution.error is None
    assert execution.execution_id is not None
    assert execution.created_at == execution.updated_at


def test_execution_success():
    execution = Execution.create()
    old_updated_at = execution.updated_at
    execution.succeed("done")
    assert execution.status == ExecutionStatus.SUCCEEDED
    assert execution.result == "done"
    assert execution.error is None
    assert execution.updated_at >= old_updated_at

def test_execution_can_fail():
    execution = Execution.create()

    execution.fail("timeout")

    assert execution.status == ExecutionStatus.FAILED
    assert execution.error == "timeout"
    assert execution.result is None

def test_succeeded_execution_cannot_fail():
    execution = Execution.create()
    execution.succeed("done")

    with pytest.raises(InvalidExecutionTransition):
        execution.fail("timeout")

def test_success_requires_result():
    execution = Execution.create()

    with pytest.raises(ValueError):
        execution.succeed(None)

def test_failure_requires_error():
    execution = Execution.create()

    with pytest.raises(ValueError):
        execution.fail(None)