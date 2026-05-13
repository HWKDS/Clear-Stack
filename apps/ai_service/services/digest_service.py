from collections import defaultdict
from datetime import UTC, datetime

from apps.ai_service.models.digest import DigestItem, DigestResponse
from apps.ai_service.models.notification import NotificationRecord


def build_digest(notifications: list[NotificationRecord], limit: int = 20) -> DigestResponse:
    selected = sorted(notifications, key=lambda item: item.priority_score, reverse=True)[:limit]
    grouped: dict[str, list[NotificationRecord]] = defaultdict(list)
    for notification in selected:
        grouped[notification.source].append(notification)

    items: list[DigestItem] = []
    for source, source_items in grouped.items():
        top_priority = max(item.priority_score for item in source_items)
        items.append(DigestItem(source=source, count=len(source_items), top_priority=top_priority))

    average_priority = 0.0
    if selected:
        average_priority = sum(item.priority_score for item in selected) / len(selected)

    highlights = [
        f"[{item.source}] {item.title} ({item.priority_score})"
        for item in selected[:5]
    ]

    return DigestResponse(
        generated_at=datetime.now(UTC),
        total_notifications=len(selected),
        average_priority=round(average_priority, 2),
        items=sorted(items, key=lambda item: item.top_priority, reverse=True),
        highlights=highlights,
    )