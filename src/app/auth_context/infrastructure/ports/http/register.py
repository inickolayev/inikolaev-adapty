from fastapi import APIRouter, status

from app.auth_context.applications.user import user_app_impl
from app.auth_context.domains.dto.user import RegisterDTO, UserDTO

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED, summary='Register a new user')
async def auth_register(data: RegisterDTO) -> UserDTO:
    user = await user_app_impl.register(data)
    return UserDTO(user_id=user.user_id, email=user.email, is_email_confirmed=user.is_email_confirmed)
