# Same async-flavoured SQLAlchemy imports as the previous slide.

from auth.utils import hash_password
from employees import service as employee_service
from models.employee import Employee
from exceptions import NotFoundException

# The function under test.
import pytest


async def test_get_by_id_returns_seeded_employee(db_session):

    seeded = Employee(
        name="Ada",
        email="ada@example.com",
        role="Developer",
        password_hash=hash_password("secret123"),
    )
    db_session.add(seeded)

    await db_session.commit()

    await db_session.refresh(seeded)

    fetched = await employee_service.get_employees_by_id(seeded.id, db_session)

    assert fetched.id == seeded.id
    assert fetched.email == "ada@example.com"


# `pytest` (not `pytest_asyncio`) is what provides `pytest.raises`. The two
# libraries cooperate — pytest is the framework; pytest-asyncio is a plugin
# that adds async-fixture support. You never swap one for the other.


# Our domain exception — raised by the service when a row is missing.


# `async def` because the body uses `await`. The `db_session` fixture comes
# from `conftest.py` — pytest-asyncio drives this on the event loop for us.
async def test_get_by_id_raises_when_missing(db_session):

    # Step 1: the exception itself
    # `pytest.raises(...)` is a context manager that *expects* the block to
    # raise the given exception. If it does → test passes. If it raises
    # something else → test fails. If it raises nothing → test fails too
    # `as exc_info` captures a handle on the raised exception for later checks.
    with pytest.raises(NotFoundException) as exc_info:
        # `get_by_id` is `async def`, so we `await` it. The `await` lives
        # *inside* the `with` block — that's the call we expect to raise.
        await employee_service.get_employees_by_id(9999, db_session)

    # Step 2: details about the exception
    # `exc_info.value` is the actual exception object (a NotFoundException).
    # Our base `AppException` exposes `.detail` — we assert the missing ID
    # appears in it, locking in "this exception with this content", not just
    # "some NotFoundException was raised somewhere".
    assert "9999" in exc_info.value.detail
