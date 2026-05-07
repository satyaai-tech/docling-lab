from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    docling_base_url: str = "http://127.0.0.1:5001"
    docling_api_key: str | None = None
    default_tenant_id: str | None = None
    request_timeout_seconds: float = 120.0


settings = Settings()
