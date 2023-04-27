"""Модуль описывающий бизнес логику работы с событиями."""
from functools import lru_cache
from logging import getLogger
from typing import AsyncIterator
from uuid import UUID

from core.config import settings
from db.database import get_db_session
from esb.base_esb import BaseESB, get_esb
from fastapi import Depends
from models.api.v1.events import NotificationEvent
from models.base import Message
from models.db import NotificationHistory
from sqlalchemy import orm, select

logger = getLogger(settings.logger_name)


class EventService(object):
    """Класс описывающий бизнес логику работы с событиями."""

    def __init__(self, esb: BaseESB, db_session: orm.Session):
        """Инициализация объекта класса.

        Args:
            esb: корпоративная шина данных/брокер сообщений.
            db_session: SQLAlchemy Session.
        """
        self.esb = esb
        self.db_session = db_session

    async def put_notification_to_queue(self, notification_event: NotificationEvent):
        """Поставить оповещение в очередь.

        Args:
            notification_event: событие оповещение.
        """
        message = Message(
            delivery_type=notification_event.delivery_type,
            event_type=notification_event.event_type,
            body=notification_event,
        )
        await self.esb.post(routing_key=notification_event.delivery_type.value, message=message)

    async def show_notification_by_user(
            self,
            user_id: UUID,
            offset: int,
            limit: int,
    ) -> AsyncIterator[NotificationHistory]:
        """Показать оповещения по пользователю из БД.

        Args:
            user_id: UUID пользователя.
            offset: количество пропускаемых сообщений.
            limit: количество отображаемых сообщений.

        Yields:
            событие нотификации.
        """
        async with self.db_session.begin() as session:
            stmt = select(NotificationHistory).\
                where(NotificationHistory.user_id == user_id).\
                order_by(NotificationHistory.created.desc()).\
                limit(limit).\
                offset(offset)
            history = await session.execute(stmt)
            for row in history.scalars():
                yield row


@lru_cache()
def get_event_service(
        ebs: BaseESB = Depends(get_esb),
        db_session: orm.Session = Depends(get_db_session),
) -> EventService:
    """Создать объект класса EventsService.

    Args:
        ebs: корпоративная шина данных/брокер сообщений.
        db_session: SQLAlchemy Session.

    Returns:
        Объект класса EventsService.
    """
    return EventService(esb=ebs, db_session=db_session)
