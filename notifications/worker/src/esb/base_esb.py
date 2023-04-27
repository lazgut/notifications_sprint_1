"""Модуль для получения ESB из списка поддерживаемых."""
from typing import Optional, Union

from esb.abstract_esb import BaseESB
from esb.rabbitmq.rabbitmq_esb import RabbitMQ

esb: Optional[Union[BaseESB, RabbitMQ]] = None


def get_esb() -> Optional[Union[BaseESB, RabbitMQ]]:
    """Получение ESB из списка поддерживаемых.

    Returns:
        Шина данных или брокер сообщений проекта

    """
    return esb
