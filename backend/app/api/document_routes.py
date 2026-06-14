from pathlib import Path

from app.api.dependencies import get_db
from app.models.chunk import Chunk
from app.models.document import Document, DocumentStatus
from app.services.chunking import ChunkingService
from app.services.document_processing import DocumentProcessingService
from app.services.embedding import EmbeddingService
from app.services.pdf import PDFService
from fastapi import APIRouter, BackgroundTasks, Depends, File, UploadFile
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/documents",
    tags=["documents"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.get("/")
def list_documents(
    db: Session = Depends(get_db),
):
    documents = db.query(Document).all()
    

    return documents


@router.post("/upload")
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    contents = await file.read()

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as f:
        f.write(contents)

    document = Document(
        name=file.filename,
        file_size=len(contents),
        status=DocumentStatus.UPLOADED,
    )

    db.add(document)
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
