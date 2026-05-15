from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.auth_context.applications.user import user_app_impl
from app.auth_context.domains.entities.user import User
from app.auth_context.domains.errors.token import InvalidTokenError

bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)]) -> User:
    if credentials is None:
        raise InvalidTokenError()
    return await user_app_impl.authenticate(credentials.credentials)
