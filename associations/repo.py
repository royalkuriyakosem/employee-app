"""Associations repo"""

from sqlalchemy.ext.asyncio import AsyncSession
from models.associations import Associations
from sqlalchemy.exc import IntegrityError
from exceptions import ConflictException
from associations.schemas import AssociationCreate


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
