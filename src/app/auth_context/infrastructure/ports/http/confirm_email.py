from fastapi import APIRouter

from app.auth_context.applications.user import user_app_impl
from app.auth_context.domains.dto.user import UserDTO

router = APIRouter()


@router.get('/{token}/', summary='Confirm email via a one-time link')
async def auth_confirm_email(token: str) -> UserDTO:
    user = await user_app_impl.confirm_email(token)
    return UserDTO(user_id=user.user_id, email=user.email, is_email_confirmed=user.is_email_confirmed)
