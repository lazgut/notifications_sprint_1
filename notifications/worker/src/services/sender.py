"""Модуль описывающий класс Sender.

Отвечает за отправку нотификаций.
"""
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from typing import Any
from uuid import UUID, uuid4

from core.config import settings
from models.db import NotificationHistory
from sqlalchemy import Engine, insert, orm


class Sender(object):
    """Класс отвечающий за рассылку оповещений."""

    def __init__(self, db_engine: Engine, db_session: orm.Session):
        """Инициализация объекта класса.

        Args:
            db_engine: SqlAlchemy Engine.
            db_session: сессия в рамках которой отправляем запросы.
        """
        self.db_engine = db_engine
        self.db_session = db_session

    def send(self, transport: str, subject: str, messages: dict[UUID, dict[str, Any]]):
        """Отправить сообщения.

        Args:
            transport: транспорт сообщения.
            subject: тема сообщения.
            messages: словарь с сообщения и данными для отправки.
        """
        if transport == 'email':
            self.send_email(subject, messages)

    def send_email(self, subject: str, messages: dict[UUID, dict[str, Any]]):
        """Отправить сообщения по почте.

        Args:
            subject: тема сообщения.
            messages: словарь с сообщения и данными для отправки.
        """
        with smtplib.SMTP(host=settings.email_host, port=settings.email_port) as smtp:
            sql_batch = []
            for user_id, message in messages.items():
                sql_insert: list[dict[str, Any]] = []
                context = message.get('context')
                if context is None:
                    context = {}
                msg = MIMEText(_text=str(message.get('message')))
                msg['Subject'] = subject
                msg['From'] = settings.email_from
                msg['To'] = str(context.get('email'))
                notification_info = {
                    'id': uuid4(),
                    'created': datetime.now(),
                    'modified': datetime.now(),
                    'user_id': user_id,
                    'transport': 'email',
                    'send': True,
                    'subject': subject,
                    'message': message.get('message'),
                }
                try:
                    smtp.sendmail(msg['From'], msg['To'], msg.as_string())
                except Exception:
                    notification_info['send'] = False

                if len(sql_insert) == settings.sql_batch_size:
                    sql_batch.append(sql_insert)
                    sql_insert = []

                sql_insert.append(notification_info)

            sql_batch.append(sql_insert)

            with self.db_engine.connect() as conn:
                for batch in sql_batch:
                    conn.execute(
                        insert(NotificationHistory),
                        batch,
                    )
                    conn.commit()
