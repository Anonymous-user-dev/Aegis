import pytest
from app.core.security import hash_password, verify_password

def test_password_is_not_plain_string():
    password = "2323dgfd2"

    hashed_password = hash_password(password)

    assert hashed_password != password

    verification = verify_password(password=password, hashed_password=hashed_password)

    assert verification is True

    wrong_password = "wrong"

    verification_2 = verify_password(password=wrong_password, hashed_password=hashed_password)

    assert verification_2 is False
