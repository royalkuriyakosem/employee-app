from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from exceptions import UnauthorizedException
from auth.utils import decode_access_token
from auth.schemas import TokenPayload


Oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(Oauth2_scheme)) -> TokenPayload:
    payload = decode_access_token(token)
    
    if payload is None:
        raise UnauthorizedException("Invalid or expired token")
    
    return TokenPayload(**payload)