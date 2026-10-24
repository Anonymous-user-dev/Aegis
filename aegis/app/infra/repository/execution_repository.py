from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from app.application.query_types import SortOrder, ExecutionSort
from app.domain.execution import Execution
from app.infra.database.mappers import execution_to_domain, execution_to_model
from app.infra.database.models import ExecutionModel, ExecutionStatus


class ExecutionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    def add(self, execution: Execution) -> None:
        model = execution_to_model(execution=execution)
        self.session.add(model)

    async def get_by_id(self, execution_id: UUID) -> Execution | None:
        stmt = select(ExecutionModel).where(
        ExecutionModel.execution_id == execution_id
    )

        result = await self.session.execute(stmt)

        model = result.scalar_one_or_none()

        if model is None:
            return None

        return execution_to_domain(model)

    async def list(self, limit: int, offset: int, status: ExecutionStatus | None = None, sort_order: SortOrder = SortOrder.ASC,    sort_executions: ExecutionSort = ExecutionSort.CREATED_AT) -> list[Execution]:
        stmt = select(ExecutionModel)

        if status is not None:
            stmt = stmt.where(
            ExecutionModel.status == status
        )

        if sort_executions == ExecutionSort.CREATED_AT:
            sort_column = ExecutionModel.created_at

        elif sort_executions == ExecutionSort.UPDATED_AT:
            sort_column = ExecutionModel.updated_at

        if sort_order == SortOrder.ASC:
            primary_order = sort_column.asc()
            id_order = ExecutionModel.execution_id.asc()

        else:
            primary_order = sort_column.desc()
            id_order = ExecutionModel.execution_id.desc()

        stmt = (stmt.order_by(primary_order, id_order).limit(limit).offset(offset))

        result = await self.session.execute(stmt)

        models = result.scalars().all()

        return [
            execution_to_domain(model)
            for model in models
        ]
    async def update(self, execution: Execution) -> None:
        stmt = select(ExecutionModel).where(ExecutionModel.execution_id == execution.execution_id)

        result = await self.session.execute(stmt)

        model = result.scalar_one_or_none()

        if model is None:
            return

        model.status = execution.status
        model.result = execution.result
        model.error = execution.error
        model.updated_at = execution.updated_at

