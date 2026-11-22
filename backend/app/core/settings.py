from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        populate_by_name=True,
    )

    database_url: str
    redis_url: str
    groq_api_key: str
    gemini_api_key: str
    debug: bool = Field(default=False, validation_alias="APP_DEBUG")
    cors_origins: str


settings = Settings()