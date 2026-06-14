from app.core.settings import settings
from google import genai


class EmbeddingService:
    client = genai.Client(api_key=settings.gemini_api_key)

    @classmethod
    def embed(
        cls,
        text: str,
    ) -> list[float]:

        response = cls.client.models.embed_content(
            model="gemini-embedding-001",
            contents=text,
        )

        return response.embeddings[0].values
