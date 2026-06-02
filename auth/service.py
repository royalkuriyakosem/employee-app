from sqlalchemy.ext.asyncio import AsyncSession
from auth.utils import create_access_token, create_refresh_token, decode_refresh_token
from auth.utils import verify_password
from exceptions import UnauthorizedException
from employees import repo
from auth.schemas import LoginResponse


async def login_access(db: AsyncSession, email: str, password: str) -> str:
    employee = await repo.get_by_email(db, email)
    if employee is None:
        raise UnauthorizedException("Invalid email or password")

    if not verify_password(password, employee.password_hash):
        raise UnauthorizedException("Invalid email or password")

    token_access = create_access_token(
        {"id": employee.id, "email": employee.email, "role": employee.role.value}
    )
    token_refresh = create_refresh_token(
        {"id": employee.id, "email": employee.email, "role": employee.role.value}
    )
    return LoginResponse(access_token=token_access, refresh_token=token_refresh)


async def refresh_access(refresh_token) -> str:
    decode = decode_refresh_token(refresh_token)
    print(decode)
    access_token = create_access_token(
        {
            "id": decode.get("id"),
            "email": decode.get("email"),
            "role": decode.get("role"),
        }
    )
    return access_token
