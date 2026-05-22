from fastapi import APIRouter, status

from app.auth_context.applications.user import user_app_impl
from app.auth_context.domains.dto.password import PasswordResetRequestDTO

router = APIRouter()


@router.post('/', status_code=status.HTTP_204_NO_CONTENT, summary='Request a one-time password reset code')
async def auth_password_reset_request(data: PasswordResetRequestDTO) -> None:
    await user_app_impl.request_password_reset(data)
