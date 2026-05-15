from datetime import timedelta
from uuid import uuid4

from dddesign.structure.applications import Application

from config.settings import settings

from share.security.jwt import encode_token

from app.auth_context.infrastructure.repositories.refresh_token import RefreshTokenRepository, refresh_token_repository_impl

TOKEN_TYPE_REFRESH = 'refresh'


class RefreshTokenApp(Application):
    repo: RefreshTokenRepository = refresh_token_repository_impl

    async def issue(self, user_id: str) -> str:
        jti = str(uuid4())
        expires_delta = timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
        await self.repo.add(user_id=user_id, jti=jti, ttl_seconds=int(expires_delta.total_seconds()))
        return encode_token({'sub': user_id, 'jti': jti, 'type': TOKEN_TYPE_REFRESH}, expires_delta=expires_delta)

    async def verify(self, user_id: str, jti: str) -> bool:
        return await self.repo.exists(user_id=user_id, jti=jti)

    async def rotate(self, user_id: str, old_jti: str) -> str:
        await self.repo.remove(user_id=user_id, jti=old_jti)
        return await self.issue(user_id)

    async def revoke_all(self, user_id: str) -> None:
        await self.repo.remove_all(user_id=user_id)


refresh_token_app_impl = RefreshTokenApp()
