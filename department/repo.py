"""
Department repo
"""
from sqlalchemy.ext.asyncio import AsyncSession
from models.department import Department
from sqlalchemy import select
from fastapi import HTTPException, status

async def get_all_departments(db: AsyncSession):
    stmt = select(Department).where(Department.deleted_at.is_(None))
    departments = await db.scalars(stmt)
    return departments.all()

async def create_department(name: str, db: AsyncSession):
    department = Department(name=name.strip().lower())
    db.add(department)
    try: 
        await db.commit()
    except:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Department {name} already exists")
    await db.refresh(department)
    return department
