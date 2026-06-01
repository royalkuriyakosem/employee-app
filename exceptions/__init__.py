"""
Exception handling
"""


class AppException(Exception):
    """Base for all application-level errors."""

    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(detail)


class NotFoundException(AppException):
    """Requested resource does not exist."""

    # def __init__(self, detail: str):
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class ConflictException(AppException):
    """Operation conflicts with existing state (e.g. duplicate email)."""


class BadRequestException(AppException):
    """Client input is invalid in a way Pydantic validation didn't catch."""


class UnauthorizedException(AppException):
    """If email and password is wrong"""


class ForbiddenException(AppException):
    """If you don't have permission"""
