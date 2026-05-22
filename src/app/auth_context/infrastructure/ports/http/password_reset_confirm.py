from fastapi import APIRouter, status

from app.auth_context.applications.user import user_app_impl
from app.auth_context.domains.dto.password import PasswordResetConfirmDTO

router = APIRouter()


@router.post('/', status_code=status.HTTP_204_NO_CONTENT, summary='Reset password with a one-time code')
async def auth_password_reset_confirm(data: PasswordResetConfirmDTO) -> None:
    await user_app_impl.reset_password(data)
