from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime

from app.api.schemas.common import NonEmptyText


class RegisterRequest(BaseModel):
    email: EmailStr
    password: NonEmptyText
    tenant_id: NonEmptyText

class UserResponse(BaseModel):
    user_id: UUID
    email: EmailStr
    tenant_id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime