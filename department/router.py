"Address Router"

from fastapi import APIRouter, status, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from department import service



router = APIRouter(prefix="/department", tags=["Department"])

@router.get("", status_code=status.HTTP_302_FOUND)
async def get_all_departments(db: AsyncSession = Depends(get_db)):
    departments = await service.get_all_departments(db)
    return [department.to_api_dict() for department in departments]

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_department(body: dict = Body(...), db: AsyncSession = Depends(get_db)):
    name = body.get("name")
    department = await service.create_department(name, db)
    return department