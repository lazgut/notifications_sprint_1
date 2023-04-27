"""Модуль описывающий класс Worker.

Отвечает за процесс отправки нотификаций пользователям.
"""
import json
from logging import getLogger

from core.config import settings
from esb.base_esb import BaseESB
from models.db import Template
from models.message_broker import Event
from services.data_collector import DataCollector
from services.sender import Sender
from sqlalchemy import URL, create_engine, orm, select

logger = getLogger(settings.logger_name)


class Worker(object):
    """Класс Worker, который разгребает очередь сообщений, персонализирует и отправляет их."""

    def __init__(self, esb: BaseESB, queue: str):
        """Инициализация объекта класса.

        Args:
            esb: ESB с которой работаем.
            queue: очередь по которой работает Worker.

        """
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
        self.esb = esb
        self.queue = queue
        self.data_collector = DataCollector()
        self.sender = Sender(self.db_engine, self.db_session)

    def run(self):
        """Запустить Worker."""
        self.esb.consumer_create(queue=self.queue)
        self.esb.consumer.worker = self
        self.esb.consumer_start()
        self.esb.consumer_stop()

    def process_message(self, message: str):
        """Обработать сообщение из очереди.

        Args:
            message: сообщение из очереди шины данных.
        """
        try:
            event = Event(**json.loads(message)['body']['body'])
        except ValueError as exception:
            event = None
            logger.exception(
                'Ошибка при приобразовании сообщения из очереди ESB.\nПодробная информация:\n%s', exception,
            )

        if event is not None:
            stmt = select(Template).where(Template.id == event.template_id)
            template = self.db_session.scalars(stmt).one_or_none()
            if template is None:
                logger.exception('Шаблон(Template) не найден по UUID. UUID: %s', str(event.template_id))
            else:
                render_templates = self.data_collector.render_templates(
                    template=template.body_template,
                    context=event.context,
                    user_ids=event.user_ids,
                )
                self.sender.send(template.transport, template.subject, render_templates)
