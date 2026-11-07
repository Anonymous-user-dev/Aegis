import pytest
import jwt
import uuid
from app.core.security import create_access_token, decode_access_token
from app.core.config import settings


def test_access_token_can_be_created_and_decoded():
    user_id = uuid.uuid4()

    token = create_access_token(user_id=user_id, tenant_id="tenant-01")

    payload = decode_access_token(token=token)

    assert payload["sub"] == str(user_id)
    assert payload["tenant_id"] == "tenant-01"
    assert payload["type"] == "access"
    assert payload["iss"] == settings.JWT_ISSUER
    assert payload["aud"] == settings.JWT_AUDIENCE
    assert "jti" in payload
    assert "exp" in payload