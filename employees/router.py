"Employee Router"

from employees import service
from fastapi import APIRouter, Depends, Body, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from employees.schemas import (
    EmployeeCreate,
    AddressCreate,
    EmployeeResponse,
    GetEmployeeById,
    UpdateEmployee,
    AddressResponse,
)
from models.employee import EmployeeRole
from auth.dependencies import get_current_user, require_role
from auth.schemas import TokenPayload


router = APIRouter(prefix="/employee", tags=["Employees"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role(EmployeeRole.HR))],
    response_model=EmployeeResponse,
)
async def create_employee(
    body: EmployeeCreate = Body(...), db: AsyncSession = Depends(get_db)
):
    db_employee = await service.create_employee(body, db)
    return db_employee


@router.get(
    "/search",
    status_code=status.HTTP_200_OK,
    response_model=list[EmployeeResponse],
    dependencies=[Depends(require_role(EmployeeRole.HR))],
)
async def search_employee_by_name(
    employee_name: str, db: AsyncSession = Depends(get_db)
):
    employees = await service.search_employee_by_name(employee_name, db)
    return [employee for employee in employees]


@router.get(
    "/address", response_model=list[AddressCreate], status_code=status.HTTP_200_OK
)
async def get_all_address(
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    print(_current_user.role)
    addresses = await service.get_all_address(db)
    return addresses


@router.get(
    "/address/{address_id}",
    response_model=AddressResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_role(EmployeeRole.HR))],
)
async def get_address_by_id(
    address_id: int,
    db: AsyncSession = Depends(get_db),
    dependencies=[Depends(require_role(EmployeeRole.HR, EmployeeRole.DEVELOPER))],
):
    address = await service.get_address_by_id(address_id, db)
    return address


@router.delete(
    "/address/{address_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_role(EmployeeRole.HR))],
)
async def delete_address_by_id(
    address_id: int,
    db: AsyncSession = Depends(get_db),
    dependencies=[Depends(require_role(EmployeeRole.HR, EmployeeRole.DEVELOPER))],
):
    result = await service.delete_address_by_id(address_id, db)
    return result


@router.get(
    "/{employee_id}/address",
    response_model=list[AddressResponse],
    status_code=status.HTTP_201_CREATED,
)
async def get_address_by_emp_id(
    employee_id: int,
    db: AsyncSession = Depends(get_db),
    dependencies=[Depends(require_role(EmployeeRole.HR, EmployeeRole.DEVELOPER))],
):
    addresses = await service.get_address_by_emp_id(employee_id, db)
    return addresses


@router.post(
    "/{employee_id}/address",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role(EmployeeRole.HR, EmployeeRole.DEVELOPER))],
)
async def add_address(
    employee_id: int,
    address: AddressCreate = Body(...),
    db: AsyncSession = Depends(get_db),
):
    result = await service.add_address(employee_id, address, db)
    return result


@router.get("/{employee_id}", response_model=GetEmployeeById)
async def get_employees_by_id(
    employee_id: int,
    db: AsyncSession = Depends(get_db),
    dependencies=[Depends(require_role(EmployeeRole.HR))],
):
    db_employees = await service.get_employees_by_id(employee_id, db)
    return db_employees


@router.get("", response_model=list[EmployeeResponse])
async def get_all_employees(
    db: AsyncSession = Depends(get_db),
    dependencies=[Depends(require_role(EmployeeRole.HR))],
):
    db_employees = await service.get_all_employees(db)
    return [employee for employee in db_employees]


@router.delete(
    "/{employee_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_role(EmployeeRole.HR))],
)
async def delete_employees_by_id(employee_id: int, db: AsyncSession = Depends(get_db)):
    result = await service.delete_employees_by_id(employee_id, db)
    return result


@router.patch(
    "/{employee_id}",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
)
async def update_employee(
    employee_id: int,
    body: UpdateEmployee = Body(...),
    db: AsyncSession = Depends(get_db),
):
    name = body.name
    email = body.email
    employee = await service.update_employee(employee_id, db, name, email)
    return employee
