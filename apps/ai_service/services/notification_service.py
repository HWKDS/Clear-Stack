from apps.ai_service.models.notification import NotificationIn, NotificationRecord
from apps.ai_service.repositories.sql_notification_repository import sql_notification_repository
from apps.ai_service.services.pii_redaction import redact_sensitive_text


KEYWORD_WEIGHTS: dict[str, int] = {
    "urgent": 30,
    "deadline": 25,
    "meeting": 20,
    "payment": 20,
    "alert": 15,
    "reply": 10,
}


def _summarize_text(text: str) -> str:
    # Keep summaries deterministic and inexpensive while the LLM pipeline evolves.
    cleaned = " ".join(text.split())
    if len(cleaned) <= 140:
        return cleaned
    return f"{cleaned[:137]}..."


def _score_priority(title: str, body: str) -> int:
    combined = f"{title} {body}".lower()
    score = 20
    for keyword, weight in KEYWORD_WEIGHTS.items():
        if keyword in combined:
            score += weight
    return max(0, min(100, score))


class NotificationService:
    def __init__(self, repository) -> None:
        self._repository = repository

    def ingest(self, payload: NotificationIn) -> NotificationRecord:
        processed_body = payload.body
        if payload.sensitive_data:
            processed_body = redact_sensitive_text(processed_body)

        record = NotificationRecord(
            source=payload.source,
            title=payload.title,
            body=processed_body,
            summary=_summarize_text(processed_body),
            priority_score=_score_priority(payload.title, processed_body),
            meta=payload.metadata,
        )
        return self._repository.add(record)

    def list_notifications(self, source: str | None = None, min_priority: int | None = None) -> list[NotificationRecord]:
        results = self._repository.list()
        if source:
            results = [item for item in results if item.source.lower() == source.lower()]
        if min_priority is not None:
            results = [item for item in results if item.priority_score >= min_priority]
        return results

    def get_notification(self, notification_id: str) -> NotificationRecord | None:
        return self._repository.get(notification_id)


notification_service = NotificationService(sql_notification_repository)
notification_repository = sql_notification_repository