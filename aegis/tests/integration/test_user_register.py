import pytest
from app.infra.repository.user_repository import UserRepository
from app.application.register_user import RegisterUser, RegisterUserCommand
from app.core.security import verify_password
from app.application.exceptions import EmailAlreadyRegistered

@pytest.mark.asyncio
async def test_register_user_new_email_return_user(session):
    repository = UserRepository(session)
    use_case = RegisterUser(repository)

    command = RegisterUserCommand(
        email="test@example.com",
        password="eidjwjif234",
        tenant_id="tenant-01"
    )

    await use_case.register(command=command)

    await session.flush()

    user = await repository.get_by_email("test@example.com")

    assert user is not None
    assert user.email == command.email
    assert user.tenant_id == command.tenant_id
    assert user.hashed_password != command.password # hashed password != plain_password
    assert verify_password(password=command.password, hashed_password=user.hashed_password)

@pytest.mark.asyncio
async def test_register_user_duplicate_email_return_error(session):
    repository = UserRepository(session)
    use_case = RegisterUser(repository)

    command_1 = RegisterUserCommand(
        email="test@example.com",
        password="eidjwjif234",
        tenant_id="tenant-01"
    )

    await use_case.register(command=command_1)

    await session.flush()

    command_2 = RegisterUserCommand(
        email="test@example.com",
        password="eidjwjif234",
        tenant_id="tenant-04"
    )



    with pytest.raises(EmailAlreadyRegistered):
        await use_case.register(command=command_2)

    