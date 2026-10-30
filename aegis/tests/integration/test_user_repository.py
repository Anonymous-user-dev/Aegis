import pytest
from app.infra.repository.user_repository import UserRepository
from app.domain.user import User


@pytest.mark.asyncio
async def test_user_repository_add_and_get_by_email(session):
    user = User.create(
        email="test@example.com",
        hashed_password="kmsdfkmeiwrowe342432",
        tenant_id='tenant-1'
    )

    repository = UserRepository(session)

    repository.add(user)

    await session.flush()

    loaded = await repository.get_by_email("test@example.com")

    assert loaded is not None
    assert loaded.user_id == user.user_id
    assert loaded.email == "test@example.com"
    assert loaded.hashed_password == "kmsdfkmeiwrowe342432"
    assert loaded.tenant_id == "tenant-1"
    assert loaded.is_active is True