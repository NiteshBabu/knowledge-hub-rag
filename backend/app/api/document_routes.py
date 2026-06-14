from datetime import datetime
from pathlib import Path

from app.api.dependencies import get_db
from app.core.limiter import limiter
from app.models.chunk import Chunk
from app.models.document import Document, DocumentStatus
from app.services.chunking import ChunkingService
from app.services.document_processing import DocumentProcessingService
from app.services.embedding import EmbeddingService
from app.services.pdf import PDFService
from fastapi import (APIRouter, BackgroundTasks, Depends, File, HTTPException,
                     Request, UploadFile)
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/documents",
    tags=["documents"],
)

MAX_FILE_SIZE = 3 * 1024 * 1024  # 3 MB
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.get("/")
def list_documents(
    request: Request,
    db: Session = Depends(get_db),
):
    documents = (
        db.query(Document)
        .filter(
            Document.session_id == request.headers.get("X-Session-Id"),
            Document.expires_at > datetime.utcnow(),
        )
        .all()
    )
    return documents


@router.post("/upload")
@limiter.limit("5/hour")
async def upload_document(
    background_tasks: BackgroundTasks,
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):

    if file.size > MAX_FILE_SIZE:
        raise HTTPException(
            413, "File size is large, please use file size less than 3MB"
        )
    session_id = request.headers.get("X-Session-Id")
    contents = await file.read()

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as f:
        f.write(contents)

    document = Document(
        name=file.filename,
        file_size=len(contents),
        status=DocumentStatus.UPLOADED,
        session_id=session_id,
    )

    db.add(document)
    db.query(Document).filter(Document.expires_at < datetime.utcnow()).delete()
    db.commit()

    background_tasks.add_task(
        DocumentProcessingService.process_document, document.id, str(file_path)
    )

    return {
        "id": document.id,
        "filename": document.name,
        "size": document.file_size,
        "status": document.status,
    }


@router.get("/{document_id}")
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
):
    document = db.get(
        Document,
        document_id,
    )

    return {
        "id": document.id,
        "filename": document.name,
        "size": document.file_size,
        "status": document.status,
    }


@router.get("/text")
def get_text():
    text = PDFService.extract_text("uploads/demo.pdf")

    chunks = ChunkingService.chunk_text(text)
    return chunks
