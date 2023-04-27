"""Модуль для визуализиции таблиц БД в админ панели."""

from django.contrib import admin
from notification.models import Task, Template


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    """Класс для отображения таблицы Template."""


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Класс для отображения таблицы Task."""
