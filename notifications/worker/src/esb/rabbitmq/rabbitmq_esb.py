"""Модуль реализации работы с брокером сообщений RabbitMQ."""
from esb.abstract_esb import BaseESB
from esb.rabbitmq.consumer import Consumer


class RabbitMQ(BaseESB):
    """Класс для реализации работы с брокером сообщений RabbitMQ."""

    def consumer_create(self, queue: str):
        """Метод создания RabbitMQ Consumer и помещения в self.aio_consumer.

        Args:
            queue: очередь которую разбирает worker.
        """
        self.consumer = Consumer()
        self.consumer.create(queue=queue)

    def consumer_start(self):
        """Метод запуска RabbitMQ Consumer."""
        self.consumer.run()

    def consumer_commit(self):
        """Метод помечает сообщение как обработанное."""
        self.consumer.commit()

    def consumer_stop(self):
        """Метод для остановки работы RabbitMQ Consumer."""
        self.consumer.stop()
