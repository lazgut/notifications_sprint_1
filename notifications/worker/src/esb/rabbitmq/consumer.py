"""Basic message consumer for RabbitMQ."""

import functools
from logging import getLogger
from typing import Optional

import backoff
import pika
from core.config import settings

logger = getLogger(settings.logger_name)


class Consumer(object):
    """Class Consumer for RabbitMQ."""

    def __init__(self):
        """Инициализирует свойств объекта класса."""
        self.worker = None
        self.connection = None
        self.channel = None

    @backoff.on_exception(backoff.expo, pika.exceptions.AMQPConnectionError, max_time=settings.backoff_max_time)
    def create(self, queue: str):
        """Создает соединение и канал.

        Args:
            queue: очередь которую разбирает worker.
        """
        credentials = pika.PlainCredentials(settings.rabbit_username, settings.rabbit_password)
        connection_parameters = pika.ConnectionParameters(
            host=settings.rabbit_host,
            port=settings.rabbit_port,
            credentials=credentials,
        )
        self.connection = pika.BlockingConnection(connection_parameters)

        self.channel = self.connection.channel()
        self.channel.queue_bind(
            exchange=settings.rabbit_events_exchange_name, queue=queue,
        )
        self.channel.basic_qos(prefetch_count=1)

        on_message_callback = functools.partial(
            self.on_message, userdata='on_message_userdata',
        )
        self.channel.basic_consume(queue=queue, on_message_callback=on_message_callback)

    @backoff.on_exception(backoff.expo, pika.exceptions.AMQPConnectionError, max_time=settings.backoff_max_time)
    def run(self):
        """Запускает прием сообщение по каналу."""
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """Закрывает соединение и канал."""
        self.channel.stop_consuming()
        self.connection.close()

    @backoff.on_exception(backoff.expo, pika.exceptions.AMQPConnectionError, max_time=settings.backoff_max_time)
    def commit(self, channel: pika.adapters.blocking_connection.BlockingChannel, method_frame: pika.spec.Basic.Deliver):
        """Отправляет в RabbitMQ информацию, что сообщение обработано.

        Args:
            channel: pika blocking channel
            method_frame: basic_deliver method

        """
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)

    def on_message(
            self,
            channel: pika.adapters.blocking_connection.BlockingChannel,
            method_frame: pika.spec.Basic.Deliver,
            header_frame: pika.spec.BasicProperties,
            body: bytes,
            userdata: Optional[str] = None,
    ):
        """Обрабатывает полученное сообщение.

        Args:
            channel: pika blocking channel
            method_frame: basic_deliver method
            header_frame: properties
            body: тело сообщения
            userdata: Extra user data (consumer tag)

        """
        logger.info('Delivery properties: %s, message metadata: %s', method_frame, header_frame)
        logger.info('Userdata: %s, message body: %s', userdata, body)
        self.worker.process_message(message=body.decode())
        self.commit(channel, method_frame)
