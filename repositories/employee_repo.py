"""Employee repo"""

from fastapi import HTTPException, status
from models.employee import Employee
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from datetime import datetime



async def create_employee(name: str, email: str, db: AsyncSession) -> Employee:
    db_employee = Employee(name=name.strip(), email=email.strip())
    db.add(db_employee)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Email '{email}' is already in use")
    await db.refresh(db_employee)
    return db_employee

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
async def update_employee(employee_id:int, db: AsyncSession, name:str = None, email:str = None):
    db.add(db_employee)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Email '{email.strip()}' is already in use")
    await db.refresh(db_employee)
    return db_employee.to_api_dict()

async def delete_employees_by_id(db_employee :Employee, db: AsyncSession):
    
    db_employee.deleted_at = datetime.now()
    db.add(db_employee)

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'User not found')
    await db.refresh(db_employee)
    return {"message":"Employee deleted sucessfully"}


async def search_employees_by_name(employee_name:str, db: AsyncSession):
    stmt = select(Employee).where(Employee.name.like(f"%{employee_name}%"))
    result =  await db.scalars(stmt)
    db_employee = result.all()
    return db_employee



