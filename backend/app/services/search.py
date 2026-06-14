from app.models.chunk import Chunk
from app.services.gemini_embedding import EmbeddingService
from sqlalchemy.orm import Session


class SearchService:

    @staticmethod
    def search(
        db: Session,
        query: str,
        limit: int = 5,
    ):
        query_embedding = EmbeddingService.embed(query)
        distance = Chunk.embedding.cosine_distance(query_embedding)
        return (
            db.query(Chunk)
            .order_by(distance)
            .limit(limit)
            .all()
        )
