from app.api.dependencies import get_db
from app.api.document_routes import router as document_router
from app.db.base import Base
from app.db.database import engine
from app.schemas.chat import ChatRequest
from app.services.embedding import EmbeddingService
from app.services.llm.factory import get_llm
from app.services.ragg import RAGService
from app.services.search import SearchService
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/search")
def search(q: str, db: Session = Depends(get_db)):
    results = SearchService.search(
        db,
        q,
    )

    return {
        "results": [
            {
                "chunk_id": chunk.id,
                "content": chunk.content,
            }
            for chunk in results
        ]
    }


@app.post("/chat")
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
):

    return RAGService.ask(
        db=db,
        question=request.question,
    )


app.include_router(document_router)


@app.get("/test-groq")
def test_groq():

    llm = get_llm()

    response = llm.generate("Reply with OK")

    return {"response": response}
