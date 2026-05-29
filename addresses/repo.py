"""
Adressess repo
"""
from sqlalchemy.ext.asyncio import AsyncSession

async def create_address(lin1: str, city: str, postal_code: int, country: str, db: AsyncSession):
    
    
    