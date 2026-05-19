from sqlmodel import col, select, update

from dddesign.structure.infrastructure.repositories import Repository
from ddutils.datetime_helpers import utc_now

from config.databases.postgres import Atomic

from app.auth_context.domains.entities.user import User, UserId
from app.auth_context.infrastructure.models.user import UserModel


class UserRepository(Repository):
    EXTERNAL_ALLOWED_METHODS: set[str] | None = {'exists', 'confirm_email'}

    @staticmethod
    async def get(user_id: UserId) -> User | None:
        async with Atomic() as session:
            instance = await session.get(UserModel, user_id)
            if instance is None or instance.deleted_at is not None:
                return None
            return instance.to_entity()

    @staticmethod
    async def get_by_filters(email: str) -> User | None:
        async with Atomic() as session:
            statement = select(UserModel).where(col(UserModel.email) == email, col(UserModel.deleted_at).is_(None))
            instance = (await session.exec(statement)).one_or_none()
            return instance.to_entity() if instance else None

    @staticmethod
    async def create(user: User) -> User:
        async with Atomic() as session:
            session.add(UserModel.from_entity(user))
            await session.flush()
            return user

    @staticmethod
    async def delete(user_id: UserId) -> None:
        async with Atomic() as session:
            statement = (
                update(UserModel)
                .where(col(UserModel.user_id) == user_id, col(UserModel.deleted_at).is_(None))
                .values(deleted_at=utc_now())
            )
            await session.execute(statement)

    @staticmethod
    async def confirm_email(user_id: UserId) -> None:
        async with Atomic() as session:
            statement = (
                update(UserModel)
                .where(col(UserModel.user_id) == user_id, col(UserModel.deleted_at).is_(None))
                .values(is_email_confirmed=True, email_confirmed_at=utc_now())
            )
            await session.execute(statement)

    @staticmethod
    async def exists(email: str) -> bool:
        async with Atomic() as session:
            statement = select(col(UserModel.user_id)).where(col(UserModel.email) == email, col(UserModel.deleted_at).is_(None))
            return (await session.exec(statement)).first() is not None


user_repository_impl = UserRepository()
