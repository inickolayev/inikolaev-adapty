from dddesign.structure.infrastructure.repositories import Repository

from config.databases.redis import redis_client

KEY_PREFIX = 'email_confirmation'


def _key(token: str) -> str:
    return f'{KEY_PREFIX}:{token}'


class EmailConfirmationRepository(Repository):
    EXTERNAL_ALLOWED_METHODS: set[str] | None = {'add', 'get', 'remove'}

    @staticmethod
    async def add(token: str, user_id: str, ttl_seconds: int) -> None:
        await redis_client.set(_key(token), user_id, ex=ttl_seconds)

    @staticmethod
    async def get(token: str) -> str | None:
        return await redis_client.get(_key(token))

    @staticmethod
    async def remove(token: str) -> None:
        await redis_client.delete(_key(token))


email_confirmation_repository_impl = EmailConfirmationRepository()
