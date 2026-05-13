from dataclasses import dataclass

from apps.ai_service.core.config import settings
from apps.ai_service.services.pii_redaction import redact_sensitive_text


@dataclass(frozen=True)
class ModelRoute:
    provider: str
    model_name: str
    prompt: str
    used_redaction: bool


def route_prompt(prompt: str, sensitive_data: bool = False) -> ModelRoute:
    sanitized_prompt = prompt
    used_redaction = False

    if sensitive_data and settings.redact_sensitive_text:
        sanitized_prompt = redact_sensitive_text(prompt)
        used_redaction = sanitized_prompt != prompt

    if sensitive_data and not settings.allow_cloud_for_sensitive_data:
        return ModelRoute(
            provider="local",
            model_name=settings.local_model_name,
            prompt=sanitized_prompt,
            used_redaction=used_redaction,
        )

    if settings.model_provider == "cloud":
        return ModelRoute(
            provider="cloud",
            model_name=settings.cloud_model_name,
            prompt=sanitized_prompt,
            used_redaction=used_redaction,
        )

    return ModelRoute(
        provider="local",
        model_name=settings.local_model_name,
        prompt=sanitized_prompt,
        used_redaction=used_redaction,
    )