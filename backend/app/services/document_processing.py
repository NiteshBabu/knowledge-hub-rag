import os

from app.db.database import SessionLocal
from app.models.chunk import Chunk
from app.models.document import Document, DocumentStatus
from app.services.chunking import ChunkingService
from app.services.gemini_embedding import EmbeddingService
from app.services.pdf import PDFService
from sqlalchemy.orm import Session


class DocumentProcessingService:

    @staticmethod
    def process_document(
        document_id: int,
        file_path: str,
    ):
        db: Session = SessionLocal()

        try:
            document = db.get(
                Document,
                document_id,
            )

            document.status = DocumentStatus.PROCESSING

            db.commit()

            text = PDFService.extract_text(file_path)

            chunks = ChunkingService.chunk_text(text)

            for chunk_content in chunks:

                embedding = EmbeddingService.embed(chunk_content)

                db.add(
                    Chunk(
                        document_id=document_id,
                        content=chunk_content,
                        embedding=embedding,
                    )
                )

            document.status = DocumentStatus.INDEXED

            db.commit()
            os.remove(file_path)

        except Exception:

            document.status = DocumentStatus.FAILED

            db.commit()

            raise

        finally:
            db.close()
