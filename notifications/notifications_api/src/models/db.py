"""Содержит описание моделей таблиц БД, которые нужны для работы процесса."""
from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Базовый класс для таблиц."""

    id: Mapped[UUID] = mapped_column(primary_key=True)
    created: Mapped[datetime]
    modified: Mapped[datetime]


class NotificationHistory(Base):
    """Таблица NotificationHistory.

    Описаны только необходимые поля.
    """

    __tablename__ = 'notification_history'
    __table_args__ = {'schema': 'notifications'}

    user_id: Mapped[UUID]
    transport: Mapped[str]
    send: Mapped[bool]
    subject: Mapped[str]
    message: Mapped[str]
