from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import traceback

from src.helper.auth import verify_token
from src.helper.handler import BaseAppException

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        return verify_token(credentials.credentials)

    except BaseAppException:
        raise

    except Exception as error:
        raise BaseAppException(
            code="AUTH_USER_ERROR",
            message="Authentication failed",
            payload={
                "details": str(error),
                "trace": traceback.format_exc(),
            },
            status_code=401,
        ) from error


async def get_current_admin(user=Depends(get_current_user)):

    if user.get("role") != "admin":
        raise BaseAppException(
            code="ADMIN_ACCESS_DENIED",
            message="Admin privileges required",
            payload={"role": user.get("role")},
            status_code=403,
        )

    return user