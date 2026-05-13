from apps.ai_service.core.config import settings
from apps.ai_service.services.model_router import route_prompt
from apps.ai_service.services.pii_redaction import redact_sensitive_text


def test_redacts_email_text() -> None:
    # Verifies that emails are removed from user-provided content.
    source_text = "Please email me at jane.doe@example.com for details."
    redacted_text = redact_sensitive_text(source_text)

    assert "jane.doe@example.com" not in redacted_text
    assert "[REDACTED_EMAIL]" in redacted_text
    assert redacted_text != source_text


def test_redacts_phone_text() -> None:
    # Verifies that phone numbers are removed before model routing.
    source_text = "Call me at +1 (415) 555-2671 tomorrow."
    redacted_text = redact_sensitive_text(source_text)

    assert "+1 (415) 555-2671" not in redacted_text
    assert "[REDACTED_PHONE]" in redacted_text
    assert redacted_text != source_text


def test_sensitive_prompt_routes_to_local_when_cloud_is_blocked(monkeypatch) -> None:
    # Sensitive prompts must stay local when cloud usage for sensitive data is disabled.
    monkeypatch.setattr(settings, "allow_cloud_for_sensitive_data", False)
    monkeypatch.setattr(settings, "model_provider", "cloud")

    sensitive_prompt = "Reach me at jane.doe@example.com and summarize this."
    routed = route_prompt(sensitive_prompt, sensitive_data=True)

    assert routed.provider == "local"
    assert routed.used_redaction is True
    assert "[REDACTED_EMAIL]" in routed.prompt


def test_non_sensitive_prompt_follows_configured_provider(monkeypatch) -> None:
    # Non-sensitive prompts should follow the global provider configuration.
    monkeypatch.setattr(settings, "model_provider", "cloud")

    regular_prompt = "Write a short haiku about clean architecture."
    routed = route_prompt(regular_prompt, sensitive_data=False)

    assert routed.provider == "cloud"
    assert routed.used_redaction is False
    assert routed.prompt == regular_prompt
