from fastapi import APIRouter

from app.auth_context.applications.user import user_app_impl
from app.auth_context.domains.dto.token import TokenPairDTO
from app.auth_context.domains.dto.user import LoginDTO

router = APIRouter()


@router.post('/', summary='Authenticate and receive an access/refresh token pair')
async def auth_login(data: LoginDTO) -> TokenPairDTO:
    return await user_app_impl.login(data)
