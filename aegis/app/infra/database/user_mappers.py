from app.domain.user import User
from app.infra.database.models import UserModel

def user_to_model(user: User) -> UserModel:
    return UserModel(
        user_id=user.user_id,
        email=user.email,
        hashed_password=user.hashed_password,
        tenant_id=user.tenant_id,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


def user_to_domain(model: UserModel) -> User:
    return User(
        user_id=model.user_id,
        email=model.email,
        hashed_password=model.hashed_password,
        tenant_id=model.tenant_id,
        is_active=model.is_active,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )