from dataclasses import dataclass
from app.infra.repository.user_repository import UserRepository
from app.domain.user import User
from app.application.exceptions import EmailAlreadyRegistered
from app.core.security import hash_password

@dataclass
class RegisterUserCommand:
    email: str
    password: str
    tenant_id: str


class RegisterUser:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def register(self, command: RegisterUserCommand):
        existing_user = await self.repository.get_by_email(email=command.email)
        if existing_user:
            raise EmailAlreadyRegistered
        

        user = User.create(email=command.email, hashed_password=hash_password(command.password), tenant_id=command.tenant_id)

        self.repository.add(user=user)

        return user

