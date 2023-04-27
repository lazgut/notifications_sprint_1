"""Модуль описывающий класс DataCollector.

Отвечает за обогощение данных из сторонних систем.
"""
from http import HTTPStatus
from logging import getLogger
from typing import Any
from uuid import UUID

import requests
from core.config import settings
from jinja2 import Environment

logger = getLogger(settings.logger_name)


class DataCollector(object):
    """Класс DataCollector, который получает данные из сторонних систем и обогащает context сообщения."""

    def get_users_info(self, user_ids: list[UUID]) -> list[dict[str, str]]:
        """Получить ФИ пользователя по id.

        Args:
            user_ids: id пользователей по которым хотим получить ФИ.

        Returns:
            список словарей с ключами свойств пользователя.
        """
        response = requests.post(
            url='{protocol}://{host}:{port}/{endpoint}'.format(
                protocol=settings.user_info_protocol,
                host=settings.user_info_host,
                port=settings.user_info_port,
                endpoint=settings.user_info_endpoint,
            ),
            auth=(settings.user_info_login, settings.user_info_password),
            headers={
                'accept': 'application/json',
                'Content-Type': 'application/json',
            },
            json=[str(user_id) for user_id in user_ids],
            timeout=settings.http_request_timeout,
        )

        users_info = []
        if response.status_code == HTTPStatus.OK:
            body = response.json()
            for user_info in body:
                users_info.append(
                    {
                        'first_name': user_info.get('first_name'),
                        'last_name': user_info.get('last_name'),
                        'email': user_info.get('email'),
                        'user_id': UUID(user_info.get('id')),
                    },
                )
        return users_info

    def render_templates(
            self,
            template: str,
            context: dict[str, Any],
            user_ids: list[UUID],
    ) -> dict[UUID, dict[str, Any]]:
        """Заполнить переменные в шаблоне.

        Args:
            template: шаблон который требуется заполнить.
            context: контекст переменных для заполнения шаблона.
            user_ids: список пользователей для рассылки.

        Returns:
            список словарей с ключом равным user_id и значением равным персонализированному шаблону.
        """
        templates_jinja2: dict[UUID, dict[str, Any]] = {}
        users_info = self.get_users_info(user_ids)
        for user_info in users_info:
            if '{{ first_name }}' in template and context.get('first_name') is None:
                context['first_name'] = user_info.get('first_name')
            if '{{ last_name }}' in template and context.get('last_name') is None:
                context['last_name'] = user_info.get('last_name')
            if context.get('email') is None:
                context['email'] = user_info.get('email')
            template_jinja2 = Environment(autoescape=True).from_string(template)
            user_id = user_info.get('user_id')
            if isinstance(user_id, UUID):
                templates_jinja2[user_id] = {
                    'message': template_jinja2.render(**context),
                    'context': context,  # в контесте лежат контактные данные для отправки сообщения
                }
        return templates_jinja2
