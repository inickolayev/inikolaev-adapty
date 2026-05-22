from typing import Annotated

from fastapi import APIRouter, Depends

from app.auth_context.applications.user import user_app_impl
from app.auth_context.domains.dto.user import ChangeEmailDTO, UserDTO
from app.auth_context.domains.entities.user import User
from app.auth_context.infrastructure.ports.http.dependencies import get_current_user

router = APIRouter()


@router.post('/', summary='Change the current user email (requires re-confirmation)')
async def auth_change_email(data: ChangeEmailDTO, current_user: Annotated[User, Depends(get_current_user)]) -> UserDTO:
    user = await user_app_impl.change_email(current_user.user_id, data)
    return UserDTO(user_id=user.user_id, email=user.email, is_email_confirmed=user.is_email_confirmed)
