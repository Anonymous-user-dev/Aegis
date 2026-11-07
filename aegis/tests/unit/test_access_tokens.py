import pytest
import jwt
import uuid
from app.core.security import create_access_token, decode_access_token
from app.core.config import settings
from datetime import datetime, timedelta, timezone





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

def test_expired_access_token_is_rejected():
    user_id = uuid.uuid4()
    now = datetime.now(timezone.utc)

    payload = {
        "iss": settings.JWT_ISSUER,
        "sub": str(uuid.uuid4()),
        "aud": settings.JWT_AUDIENCE,
        "iat": now - timedelta(minutes=10),
        "nbf": now - timedelta(minutes=10),
        "exp": now - timedelta(seconds=1),
        "jti": str(uuid.uuid4()),
        "type": "access",
        "tenant_id": "tenant-01"
    }

    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    with pytest.raises(jwt.ExpiredSignatureError):
        decode_access_token(token)

def test_future_nbf_token_is_rejected():
    now = datetime.now(timezone.utc)

    payload = {
        "iss": settings.JWT_ISSUER,
        "sub": str(uuid.uuid4()),
        "aud": settings.JWT_AUDIENCE,
        "iat": now,
        "nbf": now + timedelta(minutes=10),
        "exp": now + timedelta(minutes=30),
        "jti": str(uuid.uuid4()),
        "type": "access",
        "tenant_id": "tenant-01"
    }

    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    with pytest.raises(jwt.ImmatureSignatureError):
        decode_access_token(token)

def test_wrong_audience_is_rejected():
    now = datetime.now(timezone.utc)

    payload = {
        "iss": settings.JWT_ISSUER,
        "sub": str(uuid.uuid4()),
        "aud": "some-other-api",
        "iat": now,
        "nbf": now,
        "exp": now + timedelta(minutes=30),
        "jti": str(uuid.uuid4()),
        "type": "access",
        "tenant_id": "tenant-01"
    }

    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    with pytest.raises(jwt.InvalidAudienceError):
        decode_access_token(token)

def test_wrong_issuer_is_rejected():
    now = datetime.now(timezone.utc)

    payload = {
        "iss": "some-other-service",
        "sub": str(uuid.uuid4()),
        "aud": settings.JWT_AUDIENCE,
        "iat": now,
        "nbf": now,
        "exp": now + timedelta(minutes=30),
        "jti": str(uuid.uuid4()),
        "type": "access",
        "tenant_id": "tenant-01"
    }

    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    with pytest.raises(jwt.InvalidIssuerError):
        decode_access_token(token)

def test_token_signed_with_wrong_secret_is_rejected():
    now = datetime.now(timezone.utc)

    payload = {
        "iss": settings.JWT_ISSUER,
        "sub": str(uuid.uuid4()),
        "aud": settings.JWT_AUDIENCE,
        "iat": now,
        "nbf": now,
        "exp": now + timedelta(minutes=30),
        "jti": str(uuid.uuid4()),
        "type": "access",
        "tenant_id": "tenant-01"
    }

    token = jwt.encode(payload, "wrong-secret-key", algorithm=settings.JWT_ALGORITHM)

    with pytest.raises(jwt.InvalidSignatureError):
        decode_access_token(token)

def test_wrong_token_type_is_rejected():
    now = datetime.now(timezone.utc)

    payload = {
        "iss": settings.JWT_ISSUER,
        "sub": str(uuid.uuid4()),
        "aud": settings.JWT_AUDIENCE,
        "iat": now,
        "nbf": now,
        "exp": now + timedelta(minutes=30),
        "jti": str(uuid.uuid4()),
        "type": "refresh",
        "tenant_id": "tenant-01"
    }

    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    with pytest.raises(jwt.InvalidTokenError):
        decode_access_token(token)