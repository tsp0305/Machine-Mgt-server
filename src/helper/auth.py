from datetime import datetime, timedelta,timezone
from jose import jwt, JWTError
from passlib.context import CryptContext

from settings import settings
from src.helper.handler import BaseAppException

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    try:
        return pwd_context.hash(password)

    except Exception as error:
        raise BaseAppException(
            code="PASSWORD_HASH_ERROR",
            message="Failed to hash password",
            payload={"details": str(error)},
            status_code=500
        ) from error


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return pwd_context.verify(plain, hashed)

    except Exception as error:
        raise BaseAppException(
            code="PASSWORD_VERIFY_ERROR",
            message="Failed to verify password",
            payload={"details": str(error)},
            status_code=500
        ) from error


def create_access_token(data: dict) -> str:
    try:

        to_encode = data.copy()

        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({
            "exp": expire,
            "type": "access"
        })
        print(repr(settings.private_key),'------------------')

        token = jwt.encode(
            to_encode,
            settings.private_key,
            algorithm=settings.JWT_ALGORITHM
        )

        return token

    except Exception as error:
        raise BaseAppException(
            code="ACCESS_TOKEN_CREATION_ERROR",
            message="Failed to create access token",
            payload={"details": str(error)},
            status_code=500
        ) from error


def create_refresh_token(data: dict) -> str:
    try:

        to_encode = data.copy()

        expire = datetime.now(timezone.utc) + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )

        to_encode.update({
            "exp": expire,
            "type": "refresh"
        })

        token = jwt.encode(
            to_encode,
            settings.private_key,
            algorithm=settings.JWT_ALGORITHM
        )

        return token

    except Exception as error:
        raise BaseAppException(
            code="REFRESH_TOKEN_CREATION_ERROR",
            message="Failed to create refresh token",
            payload={"details": str(error)},
            status_code=500
        ) from error


def verify_token(token: str) -> dict:
    try:

        payload = jwt.decode(
            token,
            settings.JWT_PUBLIC_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        return payload

    except JWTError as error:

        raise BaseAppException(
            code="INVALID_TOKEN",
            message="Invalid or expired token",
            payload={"details": str(error)},
            status_code=401
        ) from error

    except Exception as error:

        raise BaseAppException(
            code="TOKEN_VERIFY_ERROR",
            message="Token verification failed",
            payload={"details": str(error)},
            status_code=500
        ) from error