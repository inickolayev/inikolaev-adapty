from datetime import datetime

from sqlmodel import Field

from share.sqlmodel.models.mixins.dates import DATETIME_TZ


class SoftDeleteMixin:
    deleted_at: datetime | None = Field(
        default=None,
        sa_type=DATETIME_TZ,  # type: ignore[arg-type]
        sa_column_kwargs={'nullable': True},
    )
