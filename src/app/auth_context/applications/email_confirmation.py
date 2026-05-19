from datetime import timedelta
from secrets import token_urlsafe

from dddesign.structure.applications import Application

from config.settings import settings

from app.auth_context.domains.errors.email_confirmation import InvalidConfirmationTokenError
from app.auth_context.infrastructure.repositories.email_confirmation import (
    EmailConfirmationRepository,
    email_confirmation_repository_impl,
)

EMAIL_CONFIRMATION_TTL = timedelta(hours=24)
CONFIRMATION_PATH = '/api/v1/auth/confirm-email/{token}/'


class EmailConfirmationApp(Application):
    repo: EmailConfirmationRepository = email_confirmation_repository_impl

    async def issue(self, user_id: str, email: str) -> str:
        token = token_urlsafe(32)
        await self.repo.add(token=token, user_id=user_id, ttl_seconds=int(EMAIL_CONFIRMATION_TTL.total_seconds()))
        link = f'{settings.SERVER_URL}{CONFIRMATION_PATH.format(token=token)}'
        # Email delivery is intentionally stubbed: the one-time link is written straight
        # to stdout instead of being sent. App logging is silenced while DEBUG is on,
        # so print is used deliberately to keep the link visible in the container console.
        print(f'[email-confirmation] link for {email}: {link}', flush=True)  # noqa: T201
        return token

    async def confirm(self, token: str) -> str:
        user_id = await self.repo.get(token)
        if user_id is None:
            raise InvalidConfirmationTokenError()
        await self.repo.remove(token)
        return user_id


email_confirmation_app_impl = EmailConfirmationApp()
