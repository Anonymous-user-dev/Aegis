from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.user import User
from app.infra.database.models import UserModel
from app.infra.database.user_mappers import user_to_domain, user_to_model

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    def add(self, user: User) -> None:
        model = user_to_model(user)

        self.session.add(model)

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(UserModel).where(UserModel.email == email)

        result = await self.session.execute(stmt)

        model = result.scalar_one_or_none()

        if model is None:
            return None

        return user_to_domain(model)