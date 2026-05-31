"""Employee repo"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.employee import Employee, Address
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from datetime import datetime
from exceptions import ConflictException
from employees.schemas import AddressResponse, EmployeeCreate



async def get_by_email(db:Session, email: str) -> Employee | None:
    stmt = select(Employee).where(
        Employee.email == email,
        Employee.deleted_at.is_(None)
        )
    db_email = await db.scalars(stmt)
    return db_email.first()


async def create_employee(body: EmployeeCreate, db: AsyncSession, hashed: str) -> Employee:
    address = Address(line1 = body.address.line1, city = body.address.city, postal_code = body.address.postal_code, country = body.address.country)
    employee = Employee(name=body.name, email=body.email, age=body.age, address=[address], password_hash=hashed)
    db.add(employee)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ConflictException(f"Email '{employee.email}' is already in use")
    await db.refresh(employee)
    return employee


async def get_employees_by_id(employee_id: int, db: AsyncSession):
    stmt = select(Employee).where(Employee.id == employee_id, Employee.deleted_at.is_(None))
    result = await db.scalars(stmt)
    return result.first()

async def get_all_employees(db: AsyncSession):
    stmt = select(Employee).where(Employee.deleted_at.is_(None))
    employees = await db.scalars(stmt)
    return employees.all()


async def update_employee(employee:Employee, db: AsyncSession, name:str = None, email:str = None):
    if name is not None:
        employee.name = name
    if email is not None:
        employee.email = email
    employee.updated_at = datetime.now()
    db.add(employee)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Email '{email.strip()}' is already in use")
    await db.refresh(employee)
    return employee

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



async def add_address(address: Address, db: AsyncSession) -> dict:
    db.add(address)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ConflictException(f"Address 'not added")
    await db.refresh(address)
    return {"message": "Address added sucessfully"}

async def get_all_address(db: AsyncSession) -> list[Address]:
    stmt = select(Address).where(Address.deleted_at.is_(None))
    result = await db.scalars(stmt)
    return result.all()

async def get_address_by_id(address_id: int, db: AsyncSession) -> dict:
    stmt = select(Address).where(Address.id == address_id, Address.deleted_at.is_(None))
    result = await db.scalars(stmt)
    return result.first()

async def delete_address(address: Address, db: AsyncSession) -> dict:
    address.deleted_at = datetime.now()
    db.add(address)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ConflictException(f"Address 'not deleted")
    await db.refresh(address)
    return {"message": "Address deleted sucessfully"}

async def get_address_by_emp_id(employee_id: int, db: AsyncSession) -> list[AddressResponse]:
    stmt = select(Address).where(Address.employee_id == employee_id, Address.deleted_at.is_(None))
    address = await db.scalars(stmt)
    return address.all()