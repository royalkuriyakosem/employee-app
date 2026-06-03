"""Associations repo"""

from sqlalchemy.ext.asyncio import AsyncSession
from models.associations import Associations
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from exceptions import NotFoundException, ConflictException
from associations.schemas import AssociationCreate
from datetime import datetime


async def map_associations(db: AsyncSession, body: AssociationCreate):
    employee_id = body.employee_id
    department_id = body.department_id
    associations = Associations(employee_id=employee_id, department_id=department_id)
    db.add(associations)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ConflictException("Associations not added")
    await db.refresh(associations)
    return {"message": "Employee added to the department successfully"}


async def delete_associations(db: AsyncSession, body: AssociationCreate):
    emp_id = body.employee_id
    dept_id = body.department_id
    stmt = select(Associations).where(
        Associations.employee_id == emp_id,
        Associations.department_id == dept_id,
        Associations.deleted_at.is_(None),
    )
    result = await db.scalars(stmt)
    association = result.first()
    association.deleted_at = datetime.now()
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise NotFoundException("Associations not deleted")
    return {"message": "Employee deleted from the department successfully"}


async def delete_associations_by_dept_id(db: AsyncSession, dept_id: int):
    stmt = select(Associations).where(
        Associations.department_id == dept_id, Associations.deleted_at.is_(None)
    )
    associations = await db.scalars(stmt)
    print(associations)
    for association in associations:
        print(association)
        association.deleted_at = datetime.now()
    try:
        db.add(association)
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise NotFoundException("Association not removed")
    return {"message": "Employee deleted from the department successfully"}
