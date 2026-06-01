from fastapi import FastAPI
from dataclasses import dataclass
from typing import TypedDict
from middleware import configure_middleware
from database import create_tables, get_db
from contextlib import asynccontextmanager
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Body, Depends
from models.employee import Employee
from employees.router import router as employee_router
from department.router import router as department_router
from associations.router import router as associations_router
from config import settings
from exceptions.handlers import register_exception_handler
from auth.router import router as auth_router
import logging



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield

app = FastAPI(
    title="Employee App",
    description="A web app for employee management system",
    version="1.0.0",
    lifespan=lifespan
)

configure_middleware(app)
app.exception_handler(register_exception_handler(app))
app.include_router(employee_router)
app.include_router(department_router)
app.include_router(auth_router)
app.include_router(associations_router)


@app.get("/health", tags=["root"])
def root():
    return {
        "status" : "healthy",
        "message": "Welcome to Employee App",
        "env" : settings.app_env

    }




# @dataclass
# class Employee:
#     name : str
#     email : str
#     # department : str
#     # salary : int
#     # hire_date : str
#     # is_deleted : None



# class CreateEmployeeResponse(TypedDict):
#     id : int
#     name : str
#     email : str
#     # department : str
#     # salary : int
#     # hire_date : str
#     # is_deleted : None


_employee={}
_id = 0

def get_next_id():
    return _id+1


# @app.get("/employee", tags=["Employees"])
# async def get_all_employees(db: AsyncSession = Depends(get_db)):
#     stmt = select(Employee).where(Employee.deleted_at.is_(None))
#     result = await db.scalars(stmt)
#     return [r.to_api_dict() for r in result.all()]

#TODO
#check if the employee is deleted
#if it is raise and exception
# @app.get("/employee/{employee_id}", tags=["Employees"])
# async def get_employees_by_id(employee_id , db: AsyncSession = Depends(get_db)):
#     stmt = select(Employee).where(Employee.id == int(employee_id))
#     result = await db.scalars(stmt)
#     # return [r.to_api_dict() for r in result.all()]
#     return result.all()


# @app.post("/employee", status_code=status.HTTP_201_CREATED, tags=["Employees"])
# async def create_employee(body: dict = Body(...), db: AsyncSession = Depends(get_db)):
#     name = body.get("name")
#     email = body.get("email")
#     if not isinstance(name, str) or not name.strip():
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="name must be a non-empty string")
#     if not isinstance(email, str) or not email.strip():
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email must be a non-empty string")
#     db_employee = Employee(name=name.strip(), email=email.strip())
#     db.add(db_employee)
#     try:
#         await db.commit()
#     except IntegrityError:
#         await db.rollback()
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Email '{email.strip()}' is already in use")
#     await db.refresh(db_employee)
#     return db_employee.to_api_dict()


#TODO
#check if the employee is deleted
#if it is raise and exception
# @app.patch("/employee/{employee_id}", status_code=status.HTTP_201_CREATED, tags=["Employees"])
# async def create_employee(employee_id:int, body: dict = Body(...), db: AsyncSession = Depends(get_db)):
#     stmt = select(Employee).where(Employee.id == employee_id)
#     result = await db.scalars(stmt)
#     db_employee = result.first()

#     if not db_employee or db_employee.deleted_at is NULL:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail=f'User not found')
    
#     if "name" in body:
#         db_employee.name = body.get("name")
    
#     if "email" in body:
#         db_employee.email = body.get("email")
#     db.add(db_employee)
#     try:
#         await db.commit()
#     except IntegrityError:
#         await db.rollback()
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Email '{email.strip()}' is already in use")
#     await db.refresh(db_employee)
#     return db_employee.to_api_dict()


# @app.delete("/employee/{employee_id}", status_code=status.HTTP_200_OK, tags=["employee"])
# async def delete_employees_by_id(employee_id : int, db : AsyncSession = Depends(get_db)):
#     stmt = select(Employee).where(Employee.id == employee_id)
#     result = await db.scalars(stmt)
#     db_employee = result.first()

#     if not db_employee or db_employee.deleted_at is NULL:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail=f'User not found')
    
#     # db_employee.deleted_at = 

#     db.add(db_employee)

#     try:
#         await db.commit()
#     except IntegrityError:
#         await db.rollback()
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'User not found')
#     await db.refresh(db_employee)
#     return {"message":"Employee deleted sucessfully"}



if __name__ == "__main__":
    main() # type: ignore
