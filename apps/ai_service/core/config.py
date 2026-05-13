from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "ClearStack AI Service"
    model_provider: str = "local"
    local_model_name: str = "llama3.1"
    cloud_model_name: str = "gpt-4o-mini"
    cloud_api_base_url: str = "https://api.openai.com/v1"
    cloud_api_key: str = ""
    ollama_base_url: str = "http://127.0.0.1:11434"
    request_timeout_seconds: float = 60.0
    redact_sensitive_text: bool = True
    allow_cloud_for_sensitive_data: bool = False
    service_api_key: str = ""
    rate_limit_per_minute: int = 60
    database_url: str = "sqlite:///./clearstack.db"


settings = Settings()