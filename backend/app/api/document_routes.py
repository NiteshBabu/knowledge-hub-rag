from pathlib import Path

from app.api.dependencies import get_db
from app.models.chunk import Chunk
from app.models.document import Document, DocumentStatus
from app.services.chunking import ChunkingService
from app.services.pdf import PDFService
from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/documents",
    tags=["documents"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/upload")
async def upload_document(
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
    db.flush()

    text = PDFService.extract_text(file_path)
    chunks = ChunkingService.chunk_text(text)

    for chunk_content in chunks:
        chunk = Chunk(document_id=document.id, content=chunk_content)
        db.add(chunk)

    document.status = DocumentStatus.INDEXED
    
    db.commit()

    return {
        "id": document.id,
        "filename": document.name,
        "size": document.file_size,
        "chunk_count": len(chunks),
    }


@router.get("/text")
def get_text():
    text = PDFService.extract_text("uploads/demo.pdf")

    chunks = ChunkingService.chunk_text(text)
    return chunks
