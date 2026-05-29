from exceptions import NotFoundException, ConflictException, BadRequestException
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi import Request
import logging
from exceptions import AppException


logger = logging.getLogger(__name__)

_STATUS_MAP: dict[type[AppException], int] = {
    NotFoundException: status.HTTP_404_NOT_FOUND,
    ConflictException: status.HTTP_409_CONFLICT,
    BadRequestException: status.HTTP_400_BAD_REQUEST
}

def register_exception_handler(app: FastAPI):
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        code = _STATUS_MAP.get(type(exc), status.HTTP_500_INTERNAL_SERVER_ERROR)
        return JSONResponse(
            status_code=code,
            content={"detail": str(exc)}
        )

    
        