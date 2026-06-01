from fastapi import APIRouter, Depends, Body, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from associations import service
from associations.schemas import AssociationCreate


router = APIRouter(prefix="/associations", tags=["Associations"])

@router.post("", status_code=status.HTTP_201_CREATED, tags=["Associations"])
async def create_employee(db: AsyncSession= Depends(get_db), body: AssociationCreate = Body(...)):
    result = await service.add_associations(db, body)
    return result
