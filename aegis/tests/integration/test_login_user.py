import uuid
from datetime import datetime, timezone

import pytest

from app.application.exceptions import InvalidCredentials, InactiveUser
from app.application.login_user import LoginUser, LoginUserCommand
from app.application.register_user import RegisterUser, RegisterUserCommand
from app.core.security import hash_password, decode_access_token
from app.domain.user import User
from app.infra.repository.user_repository import UserRepository

@pytest.mark.asyncio
async def test_correct_credentials_return_jwt(session):
    plain_password = "29439249f"
    email = "test@example.com"

    repository = UserRepository(session)
    register_use_case = RegisterUser(repository)
    register_command = RegisterUserCommand(
        email=email,
        password=plain_password,
        tenant_id="tenant-01"
    )

    user = await register_use_case.register(register_command)

    login_use_case = LoginUser(repository)
    login_command = LoginUserCommand(
        email=email,
        password=plain_password
    )

    token = await login_use_case.login(login_command)
    payload = decode_access_token(token)

    assert payload["sub"] == str(user.user_id)
    assert payload["tenant_id"] == user.tenant_id
    assert payload["type"] == "access"


@pytest.mark.asyncio
async def test_wrong_password_raises_invalid_credentials(session):
    repository = UserRepository(session)

    register_use_case = RegisterUser(repository)
    await register_use_case.register(
        RegisterUserCommand(
            email="test@example.com",
            password="correct-password",
            tenant_id="tenant-01",
        )
    )

    await session.flush()

    login_use_case = LoginUser(repository)

    command = LoginUserCommand(
        email="test@example.com",
        password="wrong-password",
    )

    with pytest.raises(InvalidCredentials):
        await login_use_case.login(command)


@pytest.mark.asyncio
async def test_unknown_email_raises_invalid_credentials(session):
    repository = UserRepository(session)
    login_use_case = LoginUser(repository)

    command = LoginUserCommand(
        email="does-not-exist@example.com",
        password="some-password",
    )

    with pytest.raises(InvalidCredentials):
        await login_use_case.login(command)


@pytest.mark.asyncio
async def test_inactive_user_is_rejected(session):
    repository = UserRepository(session)

    now = datetime.now(timezone.utc)

    user = User(
        user_id=uuid.uuid4(),
        email="inactive@example.com",
        hashed_password=hash_password("correct-password"),
        tenant_id="tenant-01",
        is_active=False,
        created_at=now,
        updated_at=now,
    )

    repository.add(user)

    await session.flush()

    login_use_case = LoginUser(repository)

    command = LoginUserCommand(
        email="inactive@example.com",
        password="correct-password",
    )

    with pytest.raises(InactiveUser):
        await login_use_case.login(command)