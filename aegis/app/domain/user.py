import uuid
from datetime import datetime, timezone

class User:
    def __init__(self, user_id, email, hashed_password, tenant_id, is_active, created_at, updated_at):
        self.user_id = user_id
        self.email = email
        self.hashed_password = hashed_password
        self.tenant_id = tenant_id
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def create(cls, email, hashed_password, tenant_id):
        now = datetime.now(timezone.utc)

        return cls(
            user_id=uuid.uuid4(),
            email=email,
            hashed_password=hashed_password,
            tenant_id=tenant_id,
            is_active=True,
            created_at=now,
            updated_at=now,
        )
            