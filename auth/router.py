from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from auth import service
from database.connection import get_db
from fastapi.security import OAuth2PasswordRequestForm
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Auth"])


# @router.post("/login", response_model=TokenResponse)
# async def login(body: LoginRequest, db: AsyncSession = Depends(get_db)):
#     token_access = await service.login_access(db, body.email, body.password)
#     token_refresh = await service.login_refresh(db, body.email, body.password)
#     return TokenResponse(access_token=token_access, refresh_token=token_refresh)


@router.post("/login")
async def login(
    form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    token = await service.login_access(db, form.username, form.password)
    logger.info(f"User {form.username} logged in sucessfully")
    return token


@router.post("/refresh")
async def get_refresh_token(
    refresh_token=Header(...), db: AsyncSession = Depends(get_db)
):
    token = await service.refresh_access(refresh_token)
    logger.info("Access token created using refresh token")
    return token
