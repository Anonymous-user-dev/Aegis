import uuid
import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
from app.core.config import settings

password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(*, password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)

def create_access_token(user_id: uuid.UUID, tenant_id: str) -> str:
    now = datetime.now(timezone.utc)

    expires_at = now + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "iss": settings.JWT_ISSUER,
        "sub": str(user_id),
        "aud": settings.JWT_AUDIENCE,
        "iat": now,
        "nbf": now,
        "exp": expires_at,
        "jti": str(uuid.uuid4()),
        "type": "access",
        "tenant_id": tenant_id,
    }

    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def decode_access_token(token: str) -> dict:
    payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM], issuer=settings.JWT_ISSUER, audience=settings.JWT_AUDIENCE,
                         options={
                             "require": [
                                 "iss",
                                 "sub",
                                 "aud",
                                 "iat",
                                 "nbf",
                                 "exp",
                                 "jti"
                             ]
                         })

    if payload.get("type") != "access":
        raise InvalidTokenError("Invalid token type")

    if not payload.get("tenant_id"):
        raise InvalidTokenError("Missing tenant_id")

    return payload
