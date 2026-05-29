"""Employee repo"""

from fastapi import HTTPException, status
from models.employee import Employee
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from datetime import datetime
from exceptions import ConflictException
from employees.schemas import EmployeeCreate


async def create_employee(employee: EmployeeCreate, db: AsyncSession) -> Employee:
    db.add(employee)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ConflictException(f"Email '{employee.email}' is already in use")
    await db.refresh(employee)
    return employee

async def get_employees_by_id(employee_id: int, db: AsyncSession):
    stmt = select(Employee).where(Employee.id == employee_id)
    result = await db.scalars(stmt)
    return result.first()

async def get_all_employees(db: AsyncSession):
    stmt = select(Employee).where(Employee.deleted_at.is_(None))
    employees = await db.scalars(stmt)
    return employees.all()

#TODO
# check if on arg comes in update employees
# async def update_employee(employee_id:int, db: AsyncSession, name:str = None, email:str = None):
#     db.add(db_employee)
#     try:
#         await db.commit()
#     except IntegrityError:
#         await db.rollback()
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Email '{email.strip()}' is already in use")
#     await db.refresh(db_employee)
#     return db_employee.to_api_dict()

async def delete_employees_by_id(db_employee :Employee, db: AsyncSession):
    
    db_employee.deleted_at = datetime.now()
    db.add(db_employee)
    await db.refresh(db_employee)
    return {"message":"Employee deleted sucessfully"}


async def search_employees_by_name(employee_name:str, db: AsyncSession):
    stmt = select(Employee).where(Employee.name.like(f"%{employee_name}%"))
    result =  await db.scalars(stmt)
    db_employee = result.all()
    return db_employee



