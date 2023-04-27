"""Модуль для реализации API по событиям."""
from http import HTTPStatus
from logging import getLogger
from uuid import UUID

from core.config import settings
from fastapi import APIRouter, Depends, Query, Response
from models.api.v1.events import NotificationEvent, NotificationHistory
from services.events import EventService, get_event_service

logger = getLogger(settings.logger_name)

router = APIRouter()


@router.post('/send_notification', status_code=HTTPStatus.CREATED)
async def put_notification_to_queue(
        notification_event: NotificationEvent,
        event_service: EventService = Depends(get_event_service),
) -> Response:
    """
    Отправить событие нотификации в очередь на обработку.

    Args:
        notification_event: модель нотификации `UserEvent`.
        event_service: сервис включающий в себя бизнес логику работы с оповещениями.

    Returns:
           Response: http ответ
    """
    await event_service.put_notification_to_queue(notification_event=notification_event)
    return Response(status_code=HTTPStatus.CREATED)


@router.get('/show_notification/{user_id}')
async def show_notification_by_user(
        user_id: UUID,
        offset: int = Query(default=0, alias='offset'),
        limit: int = Query(default=25, alias='limit'),
        event_service: EventService = Depends(get_event_service),
) -> list[NotificationHistory]:
    """
    Получить оповещения по пользователю.

    Args:
        user_id: UUID пользователя.
        offset: количество пропускаемых сообщений.
        limit: количество отображаемых сообщений.
        event_service: сервис включающий в себя бизнес логику работы с оповещениями.

    Returns:
        список событий нотификации.
    """
    if limit > 100:
        limit = 100

    notification_history = []
    async for event in event_service.show_notification_by_user(user_id=user_id, offset=offset, limit=limit):
        notification_history.append(NotificationHistory(
            transport=event.transport,
            send=event.send,
            subject=event.subject,
            message=event.message,
            created=event.created,
        ))
    return notification_history
