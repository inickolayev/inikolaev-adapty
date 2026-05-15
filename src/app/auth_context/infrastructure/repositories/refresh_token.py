from dddesign.structure.infrastructure.repositories import Repository

from config.databases.redis import redis_client

KEY_PREFIX = 'refresh_token'


def _key(user_id: str, jti: str) -> str:
    return f'{KEY_PREFIX}:{user_id}:{jti}'


class RefreshTokenRepository(Repository):
    EXTERNAL_ALLOWED_METHODS: set[str] | None = {'add', 'exists', 'remove', 'remove_all'}

    @staticmethod
    async def add(user_id: str, jti: str, ttl_seconds: int) -> None:
        await redis_client.set(_key(user_id, jti), '1', ex=ttl_seconds)

    @staticmethod
    async def exists(user_id: str, jti: str) -> bool:
        return bool(await redis_client.exists(_key(user_id, jti)))

    @staticmethod
    async def remove(user_id: str, jti: str) -> None:
        await redis_client.delete(_key(user_id, jti))

    @staticmethod
    async def remove_all(user_id: str) -> None:
        keys = [key async for key in redis_client.scan_iter(match=f'{KEY_PREFIX}:{user_id}:*')]
        if keys:
            await redis_client.delete(*keys)


refresh_token_repository_impl = RefreshTokenRepository()
