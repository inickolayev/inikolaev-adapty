from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.auth_context.applications.user import user_app_impl
from app.auth_context.domains.dto.user import UserDTO
from app.auth_context.domains.entities.user import User
from app.auth_context.infrastructure.ports.http.dependencies import get_current_user

router = APIRouter()


@router.get('/', summary='Get the current authenticated user')
async def user_get(current_user: Annotated[User, Depends(get_current_user)]) -> UserDTO:
    return UserDTO(user_id=current_user.user_id, email=current_user.email, is_email_confirmed=current_user.is_email_confirmed)


@router.delete('/', status_code=status.HTTP_204_NO_CONTENT, summary='Soft-delete the current user account')
async def user_delete(current_user: Annotated[User, Depends(get_current_user)]) -> None:
    await user_app_impl.delete(current_user.user_id)
