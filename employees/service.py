"Employee Service"

from employees import repo
from sqlalchemy.ext.asyncio import AsyncSession
from models.employee import Employee
from exceptions import NotFoundException, BadRequestException
from employees.schemas import EmployeeCreate
from auth.utils import hash_password
from employees.schemas import AddressCreate
from models import Address


async def create_employee(employee: EmployeeCreate, db: AsyncSession) -> Employee:
    name = employee.name
    email = employee.email
    hashed = hash_password(employee.password)
    if not isinstance(name, str) or not name.strip():
        raise BadRequestException("name must be a non-empty string")
    if not isinstance(email, str) or not email.strip():
        raise BadRequestException("email must be a non-empty string")

    db_employee = await repo.create_employee(employee, db, hashed)
    return db_employee


async def get_employees_by_id(employee_id: int, db: AsyncSession) -> Employee:
    employee = await repo.get_employees_by_id(employee_id, db)
    if employee is None:
        raise NotFoundException(f"User not found with id:{employee_id}")
    return employee


async def get_all_employees(db: AsyncSession):
    employees = await repo.get_all_employees(db)
    return employees


async def delete_employees_by_id(employee_id: int, db: AsyncSession):
    employee = await repo.get_employees_by_id(employee_id, db)
    if employee is None:
        raise NotFoundException(f"User not found with id:{employee_id}")
    result = await repo.delete_employees_by_id(employee, db)
    return result


async def update_employee(employee_id: int, db: AsyncSession, name: str, email: str):
    employee = await repo.get_employees_by_id(employee_id, db)
    if employee is None:
        raise NotFoundException(f"User not found with id:{employee_id}")
    result = await repo.update_employee(employee, db, name=name, email=email)
    return result


async def search_employee_by_name(employee_name: str, db: AsyncSession):
    employees = await repo.search_employees_by_name(employee_name, db)
    return employees


async def add_address(employee_id: int, address: AddressCreate, db: AsyncSession):
    employee = await repo.get_employees_by_id(employee_id, db)
    if employee is None:
        raise NotFoundException(f"User not found with id:{employee_id}")
    db_address = Address(
        line1=address.line1,
        city=address.city,
        postal_code=address.postal_code,
        country=address.country,
        employee_id=employee_id,
    )
    result = await repo.add_address(db_address, db)
    return result


async def get_all_address(db: AsyncSession):
    address = await repo.get_all_address(db)
    return address


async def get_address_by_id(address_id: int, db: AsyncSession) -> dict:
    address = await repo.get_address_by_id(address_id, db)
    if address is None:
        raise NotFoundException(f"Address NOT FOUND with id: {address_id}")
    return address


async def delete_address_by_id(address_id: int, db: AsyncSession):
    address = await get_address_by_id(address_id, db)
    result = await repo.delete_address(address, db)
    return result


async def get_address_by_emp_id(employee_id: int, db: AsyncSession):
    address = await repo.get_address_by_emp_id(employee_id, db)
    employee = await get_employees_by_id(employee_id, db)
    if address is None:
        raise NotFoundException("Address NOT FOUND")
    return address
