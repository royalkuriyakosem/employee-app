"Employee Service"

from fastapi import HTTPException, status
from repositories import employee_repo
from sqlalchemy.ext.asyncio import AsyncSession
from models.employee import Employee



async def create_employee(name: str, email: str, db: AsyncSession) -> Employee:

    if not isinstance(name, str) or not name.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="name must be a non-empty string")
    if not isinstance(email, str) or not email.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email must be a non-empty string")
    
    employee = await employee_repo.create_employee(name.strip(), email.strip(), db)
    return employee

async def get_employees_by_id(employee_id: int , db: AsyncSession) -> Employee:
    employee = await employee_repo.get_employees_by_id(employee_id , db)
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User not found with id:{employee_id}')
    return employee

async def get_all_employees(db: AsyncSession):
    employees = await employee_repo.get_all_employees(db)
    return employees

async def delete_employees_by_id(employee_id : int, db : AsyncSession):
    employee = await employee_repo.get_employees_by_id(employee_id , db)
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User not found with id:{employee_id}')
    result = await employee_repo.delete_employees_by_id(employee, db)
    return result

async def update_employee(employee_id:int, db: AsyncSession, name:str , email:str ):
    employee = await employee_repo.get_employees_by_id(employee_id , db)
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User not found with id:{employee_id}')
    
    
    result = await employee_repo.update_employee(employee, db, name=name, email=email)
    return result

async def search_employee_by_name(employee_name: str, db: AsyncSession):
    employees = await employee_repo.search_employees_by_name(employee_name, db)
    return employees