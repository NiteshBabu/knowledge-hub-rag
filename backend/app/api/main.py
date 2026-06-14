from app.api.dependencies import get_db
from app.api.document_routes import router as document_router
from app.core.limiter import limiter
from app.db.base import Base
from app.db.database import engine
from app.schemas.chat import ChatRequest
from app.services.llm.factory import get_llm
from app.services.ragg import RAGService
from app.services.search import SearchService
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SlowAPIMiddleware)


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
@limiter.limit("10/minute")
def chat(
    request: Request,
    body: ChatRequest,
    db: Session = Depends(get_db),
):

    return RAGService.ask(
        db=db,
        question=body.question,
    )


app.include_router(document_router)


@app.get("/test-groq")
def test_groq():

    llm = get_llm()

    response = llm.generate("Reply with OK")

    return {"response": response}
