from dddesign.structure.infrastructure.repositories import Repository

from config.databases.redis import redis_client

KEY_PREFIX = 'password_reset'


def _key(email: str) -> str:
    return f'{KEY_PREFIX}:{email}'


class PasswordResetRepository(Repository):
    EXTERNAL_ALLOWED_METHODS: set[str] | None = {'add', 'get', 'remove'}

    @staticmethod
    async def add(email: str, code: str, ttl_seconds: int) -> None:
        await redis_client.set(_key(email), code, ex=ttl_seconds)

    @staticmethod
    async def get(email: str) -> str | None:
        return await redis_client.get(_key(email))

    @staticmethod
    async def remove(email: str) -> None:
        await redis_client.delete(_key(email))


password_reset_repository_impl = PasswordResetRepository()
