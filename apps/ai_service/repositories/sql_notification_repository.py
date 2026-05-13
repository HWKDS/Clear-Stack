from typing import Iterable, List

from sqlmodel import Session, SQLModel, create_engine, select
from sqlalchemy import delete

from apps.ai_service.core.config import settings
from apps.ai_service.models.notification import NotificationRecord


DATABASE_URL = settings.database_url or "sqlite:///./clearstack.db"


def _get_engine():
    return create_engine(DATABASE_URL, echo=False)


class SQLNotificationRepository:
    def __init__(self) -> None:
        self._engine = _get_engine()
        SQLModel.metadata.create_all(self._engine)

    def add(self, record: NotificationRecord) -> NotificationRecord:
        with Session(self._engine) as session:
            session.add(record)
            session.commit()
            session.refresh(record)
            return record

    def list(self) -> List[NotificationRecord]:
        with Session(self._engine) as session:
            statement = select(NotificationRecord)
            results = session.exec(statement).all()
            return results

    def get(self, notification_id: str) -> NotificationRecord | None:
        with Session(self._engine) as session:
            return session.get(NotificationRecord, notification_id)

    def replace_all(self, records: Iterable[NotificationRecord]) -> None:
        with Session(self._engine) as session:
            session.exec(delete(NotificationRecord))
            for rec in records:
                session.add(rec)
            session.commit()


sql_notification_repository = SQLNotificationRepository()
