"""Модели таблиц БД сервиса нотификаций."""
import uuid

from django.db import models
from django.utils import timezone


class TemplateCodes(models.TextChoices):
    """Класс кодов шаблонов писем."""

    common = 'common', 'Обычное письмо'
    monthly_personal_statistic = 'monthly_personal_statistic', 'Ежемесячная персональная статистика'


class Transport(models.TextChoices):
    """Класс типов транспорта для отправки нотификаций."""

    sms = 'sms'
    email = 'email'
    push = 'push'


class NotificationStatuses(models.TextChoices):
    """Класс статусов сообщений."""

    to_send = 'pending', 'В очередь на отправку'
    done = 'done', 'Отправлено'
    cancelled = 'cancelled', 'Отменено'


class Priority(models.TextChoices):
    """Класс приоритетов сообщений."""

    high = 'high', 'Высокий приоритет'
    medium = 'medium', 'Средний приоритет'
    low = 'low', 'Низкий приоритет'


class UUIDTimeStampedMixin(models.Model):
    """Базовые поля для всех таблиц(UUID, дата создания и редактирования)."""

    class Meta:
        """Метапараметры класса."""

        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    def save(self, *args, **kwargs):
        """Save template.

        Args:
            args: позиционные аргументы.
            kwargs: именованные аргументы.
        """
        if not self.id:
            self.created = timezone.now()

        self.modified = timezone.now()
        super().save(*args, **kwargs)


class Template(UUIDTimeStampedMixin):
    """Шаблоны для рассылки."""

    class Meta:
        """Метапараметры класса."""

        db_table = 'notifications\".\"templates'
        indexes = [
            models.Index(
                fields=['transport'],
                name='transport_idx',
            ),
            models.Index(
                fields=['code'],
                name='code_idx',
            ),
            models.Index(
                fields=['title'],
                name='title_idx',
            ),
        ]

    title = models.CharField(max_length=250)
    code = models.CharField(choices=TemplateCodes.choices, max_length=50)
    transport = models.CharField(choices=Transport.choices, max_length=50, default=Transport.email)
    subject = models.TextField(blank=True)
    # шаблон может быть любым в зависимости от типа рассылки
    body_template = models.TextField()

    def __str__(self) -> str:
        """Метод формирующий представление объекта.

        Returns:
            Строка представление объекта.

        """
        return self.title


class Task(UUIDTimeStampedMixin):
    """Задачи для рассылки."""

    class Meta:
        """Метапараметры класса."""

        db_table = 'notifications\".\"tasks'
        indexes = [
            models.Index(
                fields=['priority'],
                name='priority_idx',
            ),
            models.Index(
                fields=['status', 'priority'],
                name='status_priority_idx',
            ),
        ]

    status = models.CharField(
        choices=NotificationStatuses.choices,
        max_length=50,
        default=NotificationStatuses.to_send,
    )
    priority = models.CharField(
        choices=Priority.choices,
        max_length=50,
        default=Priority.low,
    )

    template = models.ForeignKey(Template, on_delete=models.CASCADE, null=True)
    # данные по которым шаблон будет заполняться
    context = models.JSONField(default=dict)
    user_ids = models.TextField(blank=True)

    scheduled_datetime = models.DateTimeField(blank=True, null=True)
    execution_datetime = models.DateTimeField(blank=True, null=True)


class NotificationHistory(UUIDTimeStampedMixin):
    """История отправленных нотификаций пользователю."""

    class Meta:
        """Метапараметры класса."""

        db_table = 'notifications\".\"notification_history'
        indexes = [
            models.Index(
                fields=['user_id', 'transport'],
                name='user_id_transport_idx',
            ),
            models.Index(
                fields=['user_id', 'send'],
                name='user_id_send_idx',
            ),
        ]

    user_id = models.UUIDField()
    transport = models.CharField(choices=Transport.choices, max_length=50, default=Transport.email)
    send = models.BooleanField(default=False)
    subject = models.TextField(blank=True)
    message = models.TextField(blank=True)
