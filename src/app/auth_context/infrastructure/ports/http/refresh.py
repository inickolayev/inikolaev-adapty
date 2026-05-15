from fastapi import APIRouter

from app.auth_context.applications.user import user_app_impl
from app.auth_context.domains.dto.token import RefreshRequestDTO, TokenPairDTO

router = APIRouter()


@router.post('/', summary='Rotate tokens using a valid refresh token')
async def auth_refresh(data: RefreshRequestDTO) -> TokenPairDTO:
    return await user_app_impl.refresh(data.refresh_token)
