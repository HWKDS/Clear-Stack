"""Repository for API key persistence using SQLModel."""

from datetime import UTC, datetime, timedelta
from typing import Iterable

from sqlmodel import Session, select

from apps.ai_service.core.config import settings
from apps.ai_service.models.auth import APIKey


class SQLAPIKeyRepository:
    """SQLModel-backed repository for API key CRUD operations."""

    def __init__(self):
        from sqlalchemy import create_engine
        self._engine = create_engine(settings.database_url, echo=False)
        # Create tables if they don't exist
        from sqlmodel import SQLModel
        SQLModel.metadata.create_all(self._engine)

    def create(self, key: str, name: str, user_id: str | None = None, expires_at: datetime | None = None) -> APIKey:
        """Create and store a new API key."""
        api_key = APIKey(
            key=key,
            name=name,
            user_id=user_id,
            expires_at=expires_at,
        )
        with Session(self._engine) as session:
            session.add(api_key)
            session.commit()
            session.refresh(api_key)
            return api_key

    def get_by_key(self, key: str) -> APIKey | None:
        """Retrieve an API key record by its key value."""
        with Session(self._engine) as session:
            statement = select(APIKey).where(APIKey.key == key)
            api_key = session.exec(statement).first()
            return api_key

    def get_by_id(self, key_id: str) -> APIKey | None:
        """Retrieve an API key record by its ID."""
        with Session(self._engine) as session:
            statement = select(APIKey).where(APIKey.id == key_id)
            api_key = session.exec(statement).first()
            return api_key

    def list_by_user(self, user_id: str | None) -> list[APIKey]:
        """List all API keys for a user."""
        with Session(self._engine) as session:
            statement = select(APIKey).where(APIKey.user_id == user_id)
            keys = session.exec(statement).all()
            return list(keys)

    def revoke(self, key_id: str) -> bool:
        """Revoke an API key by setting is_active to False."""
        with Session(self._engine) as session:
            api_key = session.get(APIKey, key_id)
            if not api_key:
                return False
            api_key.is_active = False
            session.add(api_key)
            session.commit()
            return True

    def delete(self, key_id: str) -> bool:
        """Permanently delete an API key."""
        with Session(self._engine) as session:
            api_key = session.get(APIKey, key_id)
            if not api_key:
                return False
            session.delete(api_key)
            session.commit()
            return True

    def update_last_used(self, key_id: str) -> None:
        """Update the last_used_at timestamp for an API key."""
        with Session(self._engine) as session:
            api_key = session.get(APIKey, key_id)
            if api_key:
                api_key.last_used_at = datetime.now(UTC)
                session.add(api_key)
                session.commit()


# Singleton instance for use throughout the app
sql_api_key_repository = SQLAPIKeyRepository()
