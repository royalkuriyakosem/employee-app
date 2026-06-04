# Task 1 — Fixture + plain assert
# async def test_create_department_persists_name(db_session)

# BuildDepartmentCreate(name="Engineering").
# await department_service.create(db_session, body).
# Assert the returned object hasidset andname == "Engineering".
from department.service import get_department_by_id
from models.department import Department
from exceptions import NotFoundException
import pytest


async def test_create_department_persists_name(db_session):

    seeded = Department(name="Engineering")

    db_session.add(seeded)

    await db_session.commit()

    await db_session.refresh(seeded)

    fetched = await get_department_by_id(seeded.id, db_session)

    assert fetched.id == seeded.id
    assert fetched.name == "Engineering"


async def test_get_dept_id_when_misssing(db_session):

    with pytest.raises(NotFoundException) as exc_info:
        await get_department_by_id(999, db_session)

    assert "999" in exc_info.value.detail
