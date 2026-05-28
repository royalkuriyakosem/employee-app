"Employee Router"

from employees import service
from fastapi import APIRouter, Depends, Body , HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db


router = APIRouter(prefix="/employee", tags=["Employees"])

@router.post("", status_code=status.HTTP_201_CREATED, tags=["Employees"])
async def create_employee(body: dict = Body(...), db: AsyncSession = Depends(get_db)):
    name = body.get("name")
    email = body.get("email")
    db_employee = await service.create_employee(name, email, db)
    return db_employee.to_api_dict()

@router.get("/search", status_code=status.HTTP_200_OK, tags=["Employees"])
async def search_employee_by_name(employee_name:str, db: AsyncSession = Depends(get_db)):
    employees = await service.search_employee_by_name(employee_name, db)
    return [employee.to_api_dict() for employee in employees]

@router.get("/{employee_id}", tags=["Employees"])
async def get_employees_by_id(employee_id : int , db: AsyncSession = Depends(get_db)):
    db_employees  = await service.get_employees_by_id(employee_id , db)
    return db_employees.to_api_dict()

@router.get("", tags=["Employees"])
async def get_all_employees(db: AsyncSession = Depends(get_db)):
    db_employees  = await service.get_all_employees(db)
    return [employee.to_api_dict() for employee in db_employees]



@router.delete("/{employee_id}", status_code=status.HTTP_200_OK, tags=["Employees"])
async def delete_employees_by_id(employee_id : int, db : AsyncSession = Depends(get_db)):
    result = await service.delete_employees_by_id(employee_id, db)
    return result

@router.patch("/{employee_id}", status_code=status.HTTP_201_CREATED, tags=["Employees"])
async def update_employee(employee_id:int, body: dict = Body(...), db: AsyncSession= Depends(get_db)):
    name = body.get("name")
    email = body.get("email")
    employee = await service.update_employee(employee_id, db, name, email)
    return employee


    