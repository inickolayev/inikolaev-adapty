from datetime import timedelta
from secrets import randbelow

from dddesign.structure.applications import Application

from app.auth_context.domains.errors.password_reset import InvalidResetCodeError
from app.auth_context.infrastructure.repositories.password_reset import PasswordResetRepository, password_reset_repository_impl

PASSWORD_RESET_TTL = timedelta(minutes=15)
CODE_LENGTH = 6


class PasswordResetApp(Application):
    repo: PasswordResetRepository = password_reset_repository_impl

    async def issue(self, email: str) -> None:
        code = f'{randbelow(10**CODE_LENGTH):0{CODE_LENGTH}d}'
        await self.repo.add(email=email, code=code, ttl_seconds=int(PASSWORD_RESET_TTL.total_seconds()))
        # Email delivery is intentionally stubbed: the one-time code is written straight
        # to stdout instead of being sent. App logging is silenced while DEBUG is on,
        # so print is used deliberately to keep the code visible in the container console.
        print(f'[password-reset] code for {email}: {code}', flush=True)  # noqa: T201

    async def verify_and_consume(self, email: str, code: str) -> None:
        stored_code = await self.repo.get(email)
        if stored_code is None or stored_code != code:
            raise InvalidResetCodeError()
        await self.repo.remove(email)


password_reset_app_impl = PasswordResetApp()
