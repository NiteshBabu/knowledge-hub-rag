from datetime import datetime
from enum import Enum

from app.db.base import Base
from sqlalchemy import DateTime
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class DocumentStatus(str, Enum):
    UPLOADED = "UPLOADED"
    PROCESSING = "PROCESSING"
    INDEXED = "INDEXED"
    FAILED = "FAILED"


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(255))

    file_size: Mapped[int] = mapped_column(Integer)

    status: Mapped[DocumentStatus] = mapped_column(
        SqlEnum(DocumentStatus),
        default=DocumentStatus.UPLOADED,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )
