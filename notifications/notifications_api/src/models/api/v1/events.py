"""Модуль моделей событий по пользователями."""
from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from models.api.generic import GenericModel
from models.base import Event


class Notification(GenericModel):
    """Модель уведомления."""

    template_id: UUID
    user_ids: Optional[list[UUID]]
    context: dict[str, Any]


class NotificationEvent(Event):
    """Модель события уведомления."""

    body: Notification


class NotificationHistory(GenericModel):
    """Модель истории уведомления."""

    transport: str
    send: bool
    subject: str
    message: str
    created: datetime
