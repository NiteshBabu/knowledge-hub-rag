from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    groq_api_key: str
    gemini_api_key: str
    debug = False

    class Config:
        env_file = ".env"


settings = Settings()
