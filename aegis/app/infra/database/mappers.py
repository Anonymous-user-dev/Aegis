from app.domain.execution import Execution
from app.infra.database.models import ExecutionModel

def execution_to_model(execution: Execution) -> ExecutionModel:
    return ExecutionModel(
        execution_id=execution.execution_id,
        status=execution.status,
        result=execution.result,
        error=execution.error,
        created_at=execution.created_at,
        updated_at=execution.updated_at
    )

def execution_to_domain(model: ExecutionModel) -> Execution:
    return Execution(
        execution_id=model.execution_id,
        status=model.status,
        result=model.result,
        error=model.error,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )