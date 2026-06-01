


from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from auth import service
from database.connection import get_db
from auth.schemas import LoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["Auth"])



@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest, db: AsyncSession = Depends(get_db)):
    token_access = await service.login_access(db, body.email, body.password)
    token_refresh = await service.login_refresh(db, body.email, body.password)
    return TokenResponse(access_token=token_access, refresh_token=token_refresh)

