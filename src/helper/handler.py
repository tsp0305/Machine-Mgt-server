from typing import Any

class BaseAppException(Exception):
    def __init__(
        self,
        code: str,
        message: str,
        payload: dict[str, Any] | None = None,
        status_code: int = 500,
    ) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        self.payload = payload or {}
        super().__init__(message)


class ResourceNotFoundException(BaseAppException):
    def __init__(self, message: str, payload: dict[str, Any] | None = None) -> None:
        super().__init__(
            code="RESOURCE_NOT_FOUND",
            message=message,
            payload=payload,
            status_code=404,
        )


class ValidationException(BaseAppException):
    def __init__(self, message: str, payload: dict[str, Any] | None = None) -> None:
        super().__init__(
            code="VALIDATION_ERROR",
            message=message,
            payload=payload,
            status_code=400,
        )


class UnauthorizedException(BaseAppException):
    def __init__(self, message: str, payload: dict[str, Any] | None = None) -> None:
        super().__init__(
            code="UNAUTHORIZED",
            message=message,
            payload=payload,
            status_code=401,
        )


class DatabaseException(BaseAppException):
    def __init__(self, message: str, payload: dict[str, Any] | None = None) -> None:
        super().__init__(
            code="DATABASE_ERROR",
            message=message,
            payload=payload,
            status_code=500,
        )
