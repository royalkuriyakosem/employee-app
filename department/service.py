"""
Department Service
"""

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from department import repo
from exceptions.handlers import NotFoundException
from associations.repo import delete_associations_by_dept_id


async def get_all_departments(db: AsyncSession):
    departments = await repo.get_all_departments(db)
    return departments


async def create_department(name: str, db: AsyncSession):
    if not isinstance(name, str) or not name.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Department name must not be an empty string",
        )
    department = await repo.create_department(name, db)
    return department


async def get_department_by_id(dept_id: int, db: AsyncSession):
    department = await repo.get_department_by_id(dept_id, db)
    if not department:
        raise NotFoundException("Department NOT FOUND")
    return department


async def delete_department_by_id(dept_id: int, db: AsyncSession):
    delete_association = await delete_associations_by_dept_id(db, dept_id)
    if delete_association is not None:
        department = await get_department_by_id(dept_id, db)
        result = await repo.delete_department(department, db)
        return result
