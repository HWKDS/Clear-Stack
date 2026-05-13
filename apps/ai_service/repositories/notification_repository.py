from collections.abc import Iterable

from apps.ai_service.models.notification import NotificationRecord


class InMemoryNotificationRepository:
    def __init__(self) -> None:
        self._items: list[NotificationRecord] = []

    def add(self, record: NotificationRecord) -> NotificationRecord:
        self._items.append(record)
        return record

    def list(self) -> list[NotificationRecord]:
        return list(self._items)

    def get(self, notification_id: str) -> NotificationRecord | None:
        for item in self._items:
            if item.id == notification_id:
                return item
        return None

    def replace_all(self, records: Iterable[NotificationRecord]) -> None:
        self._items = list(records)