from app.api.document_routes import router as document_router
from app.db.base import Base
from app.db.database import engine
from fastapi import FastAPI

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(document_router)
