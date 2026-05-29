"""
Department Service
"""

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from department import repo

async def get_all_departments(db: AsyncSession):
    departments = await repo.get_all_departments(db)
    return departments

async def create_department(name: str, db: AsyncSession):
    if not isinstance(name,str) or not name.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Department name must not be an empty string")
    department = await repo.create_department(name, db)
    return department.to_api_dict()