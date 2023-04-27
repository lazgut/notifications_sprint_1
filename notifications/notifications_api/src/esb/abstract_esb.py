"""Модуль с абстрактным брокером сообщений."""
from abc import ABC, abstractmethod

from models.base import Message


class BaseESB(ABC):
    """Абстрактный класс брокера."""

    def __init__(self):
        """Инициализировать класс RabbitMQ."""
        self.connection = None
        self.exchange = None

    @abstractmethod
    async def connect(self) -> None:
        """Подключиться к брокеру."""

    @abstractmethod
    async def post(
        self,
        routing_key: str,
        message: Message,
    ) -> None:
        """Поставить сообщение в очередь.

        Args:
            routing_key: имя очереди/ключ маршрутизации сообщения.
            message: сообщение.

        """

    @abstractmethod
    async def disconnect(self) -> None:
        """Отключиться от брокера."""
