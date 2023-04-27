"""Модуль описывающий базовый класс любой модели."""
from typing import Any, Callable, Optional

import orjson
from pydantic import BaseModel


def orjson_dumps(value: Any, *, default: Optional[Callable[[Any], Any]]) -> str:
    """Сериализовать объект в orjson.

    Args:
        value: объект для сериализации
        default: default

    Returns:
        сериализованный объект.
    """
    return orjson.dumps(value, default=default).decode()


class GenericModel(BaseModel):
    """Базовая модель.

    Родитель всех моделей.
    """

    class Config(object):
        """Настройки."""

        json_loads = orjson.loads
        json_dumps = orjson_dumps
