"""Модуль для настройки параметров приложения."""

from django.apps import AppConfig


class NotificationConfig(AppConfig):
    """Класс настроек приложения."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notification'
