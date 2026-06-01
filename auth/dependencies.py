from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from exceptions import UnauthorizedException, ForbiddenException
from auth.utils import decode_access_token
from auth.schemas import TokenPayload
from models.employee import EmployeeRole


Oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(Oauth2_scheme)) -> TokenPayload:
    payload = decode_access_token(token)
    
    if payload is None:
        raise UnauthorizedException("Invalid or expired token")
    
    return TokenPayload(**payload)

def require_role(*roles: EmployeeRole):
    """Reutrn a dependency that checks the user has one of the given roles"""
    
    def role_checker(
        current_user: TokenPayload = Depends(get_current_user)
    ) -> TokenPayload:
        if current_user.role not in roles:
            raise ForbiddenException("You don't have the permission to perform this action")
        return get_current_user
    return role_checker