import enum
import uuid
from datetime import datetime, timezone

from polar.ext.sqlalchemy import GUID, IntEnum
from polar.models.mixins import ActiveRecordMixin, SerializeMixin
from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Model(DeclarativeBase, ActiveRecordMixin, SerializeMixin):
    __abstract__ = True


class TimestampedModel(Model):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, default=utc_now
    )
    modified_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True), onupdate=utc_now
    )


class RecordModel(TimestampedModel):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(GUID, primary_key=True, default=GUID.generate)


class StatusFlag(enum.Enum):
    DISABLED = 0
    ACTIVE = 1


class StatusMixin:
    status: Mapped[int] = mapped_column(
        IntEnum(StatusFlag), nullable=False, default=StatusFlag.DISABLED
    )
