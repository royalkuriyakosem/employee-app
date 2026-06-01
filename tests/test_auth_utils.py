import pytest
from auth.utils import hash_password, verify_password


@pytest.fixture
def hashed_password():
    return hash_password("test123")


def test_verify_password_accepts_correct_password(hashed_password):
    assert verify_password("test123", hashed_password)


def test_verify_password_reject_wrong_password(hashed_password):
    assert verify_password("test", hashed_password) is False


def test_verify_password_rejects_empty_string(hashed_password):
    assert verify_password("", hashed_password) is False
