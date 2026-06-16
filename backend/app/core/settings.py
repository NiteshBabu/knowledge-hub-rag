from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    redis_url: str
    groq_api_key: str
    gemini_api_key: str
    debug: bool = False
    cors_origins: str

    class Config:
        env_file = ".env"


settings = Settings()
