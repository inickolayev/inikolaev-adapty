from datetime import datetime
from uuid import UUID

from sqlalchemy import false
from sqlmodel import Field

from share.sqlmodel.models.base import BaseSQLModel
from share.sqlmodel.models.mixins.dates import DATETIME_TZ, DatesMixin
from share.sqlmodel.models.mixins.soft_delete import SoftDeleteMixin

from app.auth_context.domains.entities.user import User


class UserModel(BaseSQLModel[User], DatesMixin, SoftDeleteMixin, table=True):
    user_id: UUID = Field(primary_key=True)
    email: str = Field(unique=True)
    password_hash: str
    is_email_confirmed: bool = Field(default=False, sa_column_kwargs={'server_default': false(), 'nullable': False})
    email_confirmed_at: datetime | None = Field(
        default=None,
        sa_type=DATETIME_TZ,  # type: ignore[arg-type]
        sa_column_kwargs={'nullable': True},
    )
