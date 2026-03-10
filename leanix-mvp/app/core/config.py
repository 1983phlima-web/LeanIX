from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(default="LeanIX Architect Copilot MVP", alias="APP_NAME")
    environment: str = Field(default="local", alias="ENVIRONMENT")
    debug: bool = Field(default=True, alias="DEBUG")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    api_v1_prefix: str = Field(default="/api/v1", alias="API_V1_PREFIX")
    leanix_base_url: str = Field(alias="LEANIX_BASE_URL")
    leanix_api_token: str = Field(alias="LEANIX_API_TOKEN")
    llm_provider: str = Field(default="mock", alias="LLM_PROVIDER")
    llm_api_key: str = Field(default="replace-me", alias="LLM_API_KEY")
    llm_model: str = Field(default="gpt-4.1-mini", alias="LLM_MODEL")
    request_timeout_seconds: int = Field(default=20, alias="REQUEST_TIMEOUT_SECONDS")
    enable_suggest_mode: bool = Field(default=False, alias="ENABLE_SUGGEST_MODE")
    rag_enabled: bool = Field(default=False, alias="RAG_ENABLED")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
