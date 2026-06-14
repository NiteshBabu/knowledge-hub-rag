from app.db.base import Base
from pgvector.sqlalchemy import Vector
from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Chunk(Base):
    __tablename__ = "chunks"

    id: Mapped[int] = mapped_column(primary_key=True)

    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id"))

    content: Mapped[str] = mapped_column(Text)

    embedding: Mapped[list[float]] = mapped_column(Vector(3072))
