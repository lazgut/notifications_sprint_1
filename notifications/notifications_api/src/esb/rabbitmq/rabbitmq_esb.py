"""Модуль RabbitMQ."""
import aio_pika
import backoff
from core.config import settings
from esb.abstract_esb import BaseESB
from models.base import DeliveryType, Message
from pamqp.exceptions import AMQPFrameError


class RabbitMQ(BaseESB):
    """Класс RabbitMQ."""

    @backoff.on_exception(backoff.expo, exception=(ConnectionError, AMQPFrameError), max_time=settings.backoff_max_time)
    async def connect(self) -> None:
        """Подключиться к брокеру."""
        connection = await aio_pika.connect_robust(
            'amqp://{user}:{password}@{host}:{port}'.format(
                user=settings.rabbit_username,
                password=settings.rabbit_password,
                host=settings.rabbit_host,
                port=settings.rabbit_port,
            ),
        )
        channel = await connection.channel()
        exchange = await channel.declare_exchange(name=settings.rabbit_events_exchange_name, durable=True)

        for delivery in DeliveryType:
            queue = await channel.declare_queue(
                name=delivery.value,
                durable=True,
            )
            await queue.bind(exchange=exchange, routing_key=delivery.value)

        self.connection = connection
        self.exchange = exchange

    async def post(
        self,
        routing_key: str,
        message: Message,
    ) -> None:
        """Положить сообщение в очередь RabbitMQ.

        Args:
            routing_key: имя очереди/ключ маршрутизации сообщения.
            message: сообщение.
        """
        pika_message = aio_pika.Message(
            body=message.json().encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        )
        await self.exchange.publish(
            message=pika_message,
            routing_key=routing_key,
        )

    async def disconnect(self) -> None:
        """Отключиться от брокера."""
        if self.connection is not None:
            await self.connection.close()
