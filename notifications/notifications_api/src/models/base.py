"""Модуль базовых моделей."""
import enum

from pydantic import BaseModel


class DeliveryType(enum.Enum):  # noqa: WPS600
    """Перечисление способов доставки."""

    sms = 'sms'
    email = 'email'
    push = 'push'


class EventType(enum.Enum):
    """Перечисление типов событий."""

    notification = 'notification'
    admin = 'admin_notification'


class PriorityType(enum.Enum):
    """Перечисление приоритетов."""

    low = 'low'
    medium = 'medium'
    high = 'high'


class Message(BaseModel):
    """Модель базового сообщения."""

    delivery_type: DeliveryType
    event_type: EventType
    body: BaseModel


class Event(BaseModel):
    """Модель базового события."""

    delivery_type: DeliveryType
    event_type: EventType
    priority: PriorityType
