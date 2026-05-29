"""
adressses
"""
from fastapi import APIRouter, status, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db

router = APIRouter(prefix="/adresses", tag=["Address"])

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_address(body: dict = Body(...), db: AsyncSession=Depends(get_db)):
    line1 = body.get("line1")
    city = body.get("city")
    postal_code = body.get("postal_code")
    country = body.get("country")

    address = await 