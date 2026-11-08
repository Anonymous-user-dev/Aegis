from dataclasses import dataclass
from app.infra.repository.user_repository import UserRepository
from app.application.exceptions import InvalidCredentials, InactiveUser
from app.core.security import verify_password, create_access_token

@dataclass
class LoginUserCommand:
    email: str
    password: str

class LoginUser:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def login(self, command: LoginUserCommand) -> str:
        user = await self.repository.get_by_email(command.email)

        if user is None:
            raise InvalidCredentials

        if not verify_password(password=command.password, hashed_password=user.hashed_password):
            raise InvalidCredentials

        if not user.is_active:
            raise InactiveUser

        return create_access_token(user_id=user.user_id,tenant_id=user.tenant_id)
