from app.core.settings import settings
from app.services.llm.base import LLMProvider
from openai import OpenAI


class GroqProvider(LLMProvider):

    def __init__(self):
        self.client = OpenAI(
            api_key=settings.groq_api_key,
            base_url="https://api.groq.com/openai/v1",
        )

    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0,
        )
        

        return response.choices[0].message.content
