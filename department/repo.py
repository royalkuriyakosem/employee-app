"""
Department repo
"""

from sqlalchemy.ext.asyncio import AsyncSession
from models.department import Department
from sqlalchemy import select
from fastapi import HTTPException, status
from datetime import datetime
from exceptions.handlers import NotFoundException
from sqlalchemy.exc import IntegrityError


async def get_all_departments(db: AsyncSession):
    stmt = select(Department).where(Department.deleted_at.is_(None))
    departments = await db.scalars(stmt)
    return departments.all()


async def create_department(name: str, db: AsyncSession):
    department = Department(name=name.strip().lower())
    db.add(department)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Department {name} already exists",
        )
    await db.refresh(department)
    return department


async def get_department_by_id(dept_id: int, db: AsyncSession):
    stmt = select(Department).where(
        Department.deleted_at.is_(None), Department.id == dept_id
    )
    department = await db.scalars(stmt)
    return department.first()


# TODO
# Before delting department delete the associations to it
async def delete_department(department: Department, db: AsyncSession):
    department.deleted_at = datetime.now()
    db.add(department)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise NotFoundException("Department Not Found")
    return {"message": "Department deleted sucessfully"}
