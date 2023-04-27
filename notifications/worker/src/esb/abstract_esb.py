"""Модуль абстрактного класса BaseESB. Родитель всех ESB."""
from abc import ABC, abstractmethod


class BaseESB(ABC):
    """Абстрактный класс BaseESB."""

    def __init__(self):
        """Описываем обязательные реквизиты класса."""
        self.consumer = None

    @abstractmethod
    def consumer_create(self, queue: str):
        """Метод создания consumer и помещения в self.aio_consumer.

        Args:
            queue: очередь которую разбирает worker.
        """

    @abstractmethod
    def consumer_start(self):
        """Метод запуска consumer."""

    @abstractmethod
    def consumer_commit(self):
        """Метод для установки пометки прочтения сообщения из очереди."""

    @abstractmethod
    def consumer_stop(self):
        """Метод для остановки работы consumer."""
