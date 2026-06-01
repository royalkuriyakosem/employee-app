
from sqlalchemy.ext.asyncio import AsyncSession
from auth.utils import create_access_token, create_refresh_token
from auth.utils import verify_password
from exceptions import UnauthorizedException
from employees import repo 

async def login_access (db: AsyncSession, email: str, password: str) -> str:
    employee = await repo.get_by_email(db, email)
    if employee is None:
        raise UnauthorizedException("Invalid email or password")
    
    if not verify_password(password, employee.password_hash):
        raise UnauthorizedException("Invalid email or password")
    
    return create_access_token({"id": employee.id, "email": employee.email})

async def login_refresh (db: AsyncSession, email: str, password: str) -> str:
    employee = await repo.get_by_email(db, email)
    if employee is None:
        raise UnauthorizedException("Invalid email or password")
    
    if not verify_password(password, employee.password_hash):
        raise UnauthorizedException("Invalid email or password")
    
    return create_refresh_token({"id": employee.id, "email": employee.email})