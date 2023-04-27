"""Модуль описывающий класс Scheduler."""

import logging
from datetime import datetime
from time import sleep
from uuid import UUID

import backoff
import requests
from core.config import settings
from models.db import Task
from sqlalchemy import URL, create_engine, orm, select, update
from sqlalchemy.exc import OperationalError


class Scheduler(object):
    """Класс Scheduler. Перемещает задачи из БД в очередь брокера через API.

    Класс Scheduler, который проверяет задачи по времени необходимого исполнения
    и ставит нужные в очередь сообщений.
    """

    @backoff.on_exception(backoff.expo, OperationalError, max_time=settings.backoff_max_time)
    def __init__(self):
        """Инициализация объекта класса."""
        url_object = URL.create(
            drivername=settings.db_drivername,
            username=settings.db_username,
            password=settings.db_password,
            host=settings.db_host,
            port=settings.db_port,
            database=settings.db_database,
        )
        self.db_engine = create_engine(url_object)
        self.db_session = orm.Session(self.db_engine)
        self.url_api = '{protocol}://{host}:{port}/'.format(
            protocol=settings.api_protocol,
            host=settings.api_host,
            port=settings.api_port,
        )

    @backoff.on_exception(backoff.expo, OperationalError, max_time=settings.backoff_max_time)
    def run(self):
        """Метод запуска Scheduler."""
        while True:
            stmt = select(Task).\
                where(Task.status == 'pending').\
                where(Task.scheduled_datetime <= datetime.now())
            for task in self.db_session.scalars(stmt):
                self.send(
                    delivery_type=task.template.transport,
                    priority=task.priority,
                    user_ids=task.user_ids.split(','),
                    template_id=task.template.id,
                    context=task.context,
                )
                upd_stmt = update(Task).\
                    where(Task.id == task.id).\
                    values(
                    status='done',
                    execution_datetime=datetime.now(),
                    modified=datetime.now(),
                )
                with self.db_engine.begin() as conn:
                    conn.execute(upd_stmt)

            sleep(settings.main_process_sleep_time)

    @backoff.on_exception(backoff.expo, requests.exceptions.ConnectionError, max_time=settings.backoff_max_time)
    def send(
            self,
            delivery_type: str,
            priority: str,
            user_ids: list[str],
            template_id: UUID,
            context: dict,
    ):
        """Метод отправки запланированной рассылки на обработку.

        Raises:
            ConnectionError: ошибка подключения к API

        Args:
            delivery_type: способ рассылки
            priority: приоритет
            user_ids: список пользователей
            template_id: идентификатор шаблона
            context: контекст для шаблонов

        Returns:
            requests.Response
        """
        body = {
            'delivery_type': delivery_type,
            'event_type': 'notification',
            'priority': priority,
            'body': {
                'user_ids': user_ids,
                'template_id': str(template_id),
                'context': context,
            },
        }
        url = self.url_api + settings.api_send_notification_path
        try:
            return requests.post(url, json=body, timeout=settings.wait_timeout)
        except requests.exceptions.ConnectionError as err:
            logging.error('Trying to connect {url}.'.format(url=url))
            raise requests.exceptions.ConnectionError(err)
