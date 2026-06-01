from sqlalchemy.ext.asyncio import AsyncSession
from associations import repo
from associations.schemas import AssociationCreate




async def add_associations(db: AsyncSession, body: AssociationCreate):
    result = await repo.map_associations(db, body)
    return result