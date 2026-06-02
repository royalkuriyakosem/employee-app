"""Associations repo"""

from sqlalchemy.ext.asyncio import AsyncSession
from models.associations import Associations
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from exceptions import ConflictException
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
        Associations.employee_id == emp_id, Associations.department_id == dept_id
    )
    result = await db.scalars(stmt)
    association = result.first()
    print(association.deleted_at, datetime.now())
    association.deleted_at = datetime.now()
    print(association.deleted_at, datetime.now())

    db.add(association)
    print(association.deleted_at, datetime.now())
    try:
        await db.commit()
        await db.refresh(association)
    except IntegrityError:
        await db.rollback()
        raise ConflictException("Associations not deleted")
    print(association.deleted_at, datetime.now())
    return {"message": "Employee deleted from the department successfully"}
