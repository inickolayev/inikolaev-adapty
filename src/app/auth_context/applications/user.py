from datetime import timedelta
from typing import Any

import jwt

from dddesign.structure.applications import Application

from config.settings import settings

from share.security.jwt import decode_token, encode_token
from share.security.password import hash_password, verify_password

from app.auth_context.applications.email_confirmation import EmailConfirmationApp, email_confirmation_app_impl
from app.auth_context.applications.refresh_token import TOKEN_TYPE_REFRESH, RefreshTokenApp, refresh_token_app_impl
from app.auth_context.domains.dto.token import TokenPairDTO
from app.auth_context.domains.dto.user import LoginDTO, RegisterDTO
from app.auth_context.domains.entities.user import User, UserId
from app.auth_context.domains.errors.token import InvalidTokenError, RefreshTokenRevokedError, TokenExpiredError
from app.auth_context.domains.errors.user import (
    EmailNotConfirmedError,
    InvalidCredentialsError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from app.auth_context.infrastructure.repositories.user import UserRepository, user_repository_impl

TOKEN_TYPE_ACCESS = 'access'


class UserApp(Application):
    repo: UserRepository = user_repository_impl
    refresh_token_app: RefreshTokenApp = refresh_token_app_impl
    email_confirmation_app: EmailConfirmationApp = email_confirmation_app_impl

    async def register(self, data: RegisterDTO) -> User:
        if await self.repo.exists(email=data.email):
            raise UserAlreadyExistsError()

        user = await self.repo.create(User.factory(email=data.email, password_hash=hash_password(data.password)))
        await self.email_confirmation_app.issue(user_id=str(user.user_id), email=user.email)
        return user

    async def confirm_email(self, token: str) -> User:
        user_id = UserId(await self.email_confirmation_app.confirm(token))
        await self.repo.confirm_email(user_id)
        return await self.get(user_id)

    async def login(self, data: LoginDTO) -> TokenPairDTO:
        user = await self.repo.get_by_filters(email=data.email)
        if user is None or not verify_password(data.password, user.password_hash):
            raise InvalidCredentialsError()
        if not user.is_email_confirmed:
            raise EmailNotConfirmedError()

        return await self._issue_pair(str(user.user_id))

    async def refresh(self, refresh_token: str) -> TokenPairDTO:
        payload = self._decode(refresh_token)
        user_id = payload.get('sub')
        jti = payload.get('jti')
        if payload.get('type') != TOKEN_TYPE_REFRESH or not isinstance(user_id, str) or not isinstance(jti, str):
            raise InvalidTokenError()

        if not await self.refresh_token_app.verify(user_id=user_id, jti=jti):
            raise RefreshTokenRevokedError()

        new_refresh_token = await self.refresh_token_app.rotate(user_id=user_id, old_jti=jti)
        return TokenPairDTO(access_token=self._issue_access(user_id), refresh_token=new_refresh_token)

    async def get(self, user_id: UserId) -> User:
        user = await self.repo.get(user_id)
        if user is None:
            raise UserNotFoundError()
        return user

    async def delete(self, user_id: UserId) -> None:
        await self.repo.delete(user_id)
        await self.refresh_token_app.revoke_all(user_id=str(user_id))

    async def authenticate(self, access_token: str) -> User:
        payload = self._decode(access_token)
        user_id = payload.get('sub')
        if payload.get('type') != TOKEN_TYPE_ACCESS or not isinstance(user_id, str):
            raise InvalidTokenError()
        return await self.get(UserId(user_id))

    async def _issue_pair(self, user_id: str) -> TokenPairDTO:
        return TokenPairDTO(access_token=self._issue_access(user_id), refresh_token=await self.refresh_token_app.issue(user_id))

    @staticmethod
    def _issue_access(user_id: str) -> str:
        return encode_token(
            {'sub': user_id, 'type': TOKEN_TYPE_ACCESS},
            expires_delta=timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES),
        )

    @staticmethod
    def _decode(token: str) -> dict[str, Any]:
        try:
            return decode_token(token)
        except jwt.ExpiredSignatureError as error:
            raise TokenExpiredError() from error
        except jwt.InvalidTokenError as error:
            raise InvalidTokenError() from error


user_app_impl = UserApp()
