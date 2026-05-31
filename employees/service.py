"Employee Service"

from fastapi import HTTPException, status
from employees import repo
from sqlalchemy.ext.asyncio import AsyncSession
from models.employee import Employee
from exceptions import NotFoundException, BadRequestException
from employees.schemas import EmployeeCreate
from auth.utils import hash_password

    




async def create_employee(employee: EmployeeCreate, db: AsyncSession) -> Employee:
    name = employee.name
    email= employee.email
    hashed = hash_password(employee.password)
    if not isinstance(name, str) or not name.strip():
        raise BadRequestException("name must be a non-empty string")
    if not isinstance(email, str) or not email.strip():
        raise BadRequestException("email must be a non-empty string")
    
    db_employee = await repo.create_employee(employee, db, hashed)
    return db_employee

async def get_employees_by_id(employee_id: int , db: AsyncSession) -> Employee:
    employee = await repo.get_employees_by_id(employee_id , db)
    if employee is None:
        raise NotFoundException(f'User not found with id:{employee_id}')
    return employee

async def get_all_employees(db: AsyncSession):
    employees = await repo.get_all_employees(db)
    return employees

async def delete_employees_by_id(employee_id : int, db : AsyncSession):
    employee = await repo.get_employees_by_id(employee_id , db)
    if employee is None:
        raise NotFoundException(f'User not found with id:{employee_id}')
    result = await repo.delete_employees_by_id(employee, db)
    return result

async def update_employee(employee_id:int, db: AsyncSession, name:str , email:str ):
    employee = await repo.get_employees_by_id(employee_id , db)
    if employee is None:
        raise NotFoundException(f'User not found with id:{employee_id}')
    
    
    result = await repo.update_employee(employee, db, name=name, email=email)
    return result

async def search_employee_by_name(employee_name: str, db: AsyncSession):
    employees = await repo.search_employees_by_name(employee_name, db)
    return employees