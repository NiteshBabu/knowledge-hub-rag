from app.services.llm.factory import get_llm
from app.services.search import SearchService
from sqlalchemy.orm import Session


class RAGService:

    @staticmethod
    def ask(
        db: Session,
        question: str,
    ):

        chunks = SearchService.search(
            db=db,
            query=question,
            limit=5,
        )

        context = "\n\n".join(chunk.content for chunk in chunks)

        prompt = f"""
You are a helpful assistant.

Answer ONLY from the provided context.

If the answer is not available,
say you do not know.

Context:

{context}

Question:

{question}
"""

        llm = get_llm()

        answer = llm.generate(prompt)

        return {"answer": answer, "sources": [chunk.id for chunk in chunks]}
