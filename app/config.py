import os
from typing import Literal
from pydantic_settings import BaseSettings
from pydantic import model_validator
from app.utils.logging_config import logger

class Settings(BaseSettings):
    LOG_INFO_TO_LOGS_FILE: bool = False
    LLM_TEMPERATURE: float = 0
    LLM_PROVIDER: str | None = None
    OPENAI_API_KEY: str | None = None
    GOOGLE_API_KEY: str | None = None

    @model_validator(mode="after")
    def check_required_keys(self) -> "Settings":
        
        if not self.LLM_TEMPERATURE:
            logger.error("LLM_TEMPERATURE is missing it is required environment variable.")
            raise ValueError("LLM_TEMPERATURE is missing it is required environment variable.")

        if not self.LLM_PROVIDER:
            logger.error("LLM_PROVIDER is missing it is required environment variable.")
            raise ValueError("LLM_PROVIDER is missing it is required environment variable.")

        if self.LLM_PROVIDER == "openai" and not self.OPENAI_API_KEY:
            logger.error("OPENAI_API_KEY is required when LLM_PROVIDER is 'openai'")
            raise ValueError("OPENAI_API_KEY is required when LLM_PROVIDER is 'openai'")

        if self.LLM_PROVIDER == "gemini" and not self.GOOGLE_API_KEY:
            logger.error("GOOGLE_API_KEY is required when LLM_PROVIDER is 'gemini'")
            raise ValueError("GOOGLE_API_KEY is required when LLM_PROVIDER is 'gemini'")

        if self.LLM_PROVIDER == "anthropic":
            # If you add ANTHROPIC_API_KEY later, validate here
            pass
        return self

    class Config:
        env_file = ".env" if os.getenv("ENV", "dev") == "dev" else None

# Initialize to load + validate settings
settings = Settings()
