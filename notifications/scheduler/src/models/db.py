"""Содержит описание моделей таблиц БД, которые нужны для работы процесса."""
from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Базовый класс для таблиц."""

    id: Mapped[UUID] = mapped_column(primary_key=True)
    modified: Mapped[datetime]


class Template(Base):
    """Таблица Template.

    Описаны только необходимые поля.
    """

    __tablename__ = 'templates'
    __table_args__ = {'schema': 'notifications'}

    transport: Mapped[str]

    tasks: Mapped[list['Task']] = relationship(back_populates='template')


class Task(Base):
    """Таблица Task.

    Описаны только необходимые поля.
    """

    __tablename__ = 'tasks'
    __table_args__ = {'schema': 'notifications'}

    status: Mapped[str]
    priority: Mapped[str]
    user_ids: Mapped[str]

    context: Mapped[dict] = mapped_column(JSONB, default=dict)

    scheduled_datetime: Mapped[datetime]
    execution_datetime: Mapped[datetime]

    template_id = mapped_column(ForeignKey('notifications.templates.id'))
    template: Mapped[Template] = relationship(back_populates='tasks')
