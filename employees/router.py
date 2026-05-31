"Employee Router"

from employees import service
from fastapi import APIRouter, Depends, Body , HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from employees.schemas import EmployeeCreate, AddressCreate, EmployeeeResponse, GetEmployeeById
from models import Employee
from auth.dependencies import get_current_user
from auth.schemas import TokenPayload



router = APIRouter(prefix="/employee", tags=["Employees"])

@router.post("", status_code=status.HTTP_201_CREATED, tags=["Employees"])
async def create_employee(body: EmployeeCreate = Body(...), db: AsyncSession = Depends(get_db)):
    db_employee = await service.create_employee(body, db)
    return db_employee

@router.get("/search", status_code=status.HTTP_200_OK, response_model=list[EmployeeeResponse])
async def search_employee_by_name(employee_name:str, db: AsyncSession = Depends(get_db)):
    employees = await service.search_employee_by_name(employee_name, db)
    return [employee for employee in employees]

# @router.post("/{employee_id}/address", status_code=status.HTTP_201_CREATED)
# async def create_address(body: dict = Body(...), db: AsyncSession=Depends(get_db)):
#     line1 = body.get("line1")
#     city = body.get("city")
#     postal_code = body.get("postal_code")
#     country = body.get("country")
#     address = await 
    

@router.get("/{employee_id}", response_model=GetEmployeeById)
async def get_employees_by_id(employee_id : int , db: AsyncSession = Depends(get_db)):
    db_employees  = await service.get_employees_by_id(employee_id , db)
    return db_employees

@router.get("", response_model=list[EmployeeeResponse])
async def get_all_employees(db: AsyncSession = Depends(get_db), _current_user: TokenPayload = Depends(get_current_user)):
    db_employees  = await service.get_all_employees(db)
    return [employee for employee in db_employees]



@router.delete("/{employee_id}", status_code=status.HTTP_200_OK)
async def delete_employees_by_id(employee_id : int, db : AsyncSession = Depends(get_db)):
    result = await service.delete_employees_by_id(employee_id, db)
    return result

@router.patch("/{employee_id}", status_code=status.HTTP_201_CREATED)
async def update_employee(employee_id:int, body: EmployeeeResponse = Body(...), db: AsyncSession= Depends(get_db)):
    name = body.get("name")
    email = body.get("email")
    employee = await service.update_employee(employee_id, db, name, email)
    return employee

