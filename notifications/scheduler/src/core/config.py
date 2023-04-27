"""Модуль описывающий переменные проекта."""

import json
import os
from typing import Any

from pydantic import BaseSettings, Field

# Корень проекта
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)),
)

ENV_FILE_PATH = os.path.join(BASE_DIR, 'core', '.env')


def list_parse_fallback(json_str: str) -> Any:
    """Функция для парсинга json объектов и list объектов.

    Args:
        json_str: строка с сериализованным объектом(json. list).

    Returns:
        десериализованный из json объект или list.

    """
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return json_str.split(',')


class Settings(BaseSettings):
    """Класс переменных проекта."""

    base_dir: str = Field(BASE_DIR)

    # Настройки API
    api_protocol: str = Field(..., env='API_PROTOCOL')
    api_host: str = Field(..., env='API_HOST')
    api_port: int = Field(..., env='API_PORT')
    api_send_notification_path: str = Field(..., env='API_SEND_NOTIFICATION_PATH')

    # Настройки БД
    db_drivername: str = Field(..., env='DB_DRIVER_NAME')
    db_host: str = Field(..., env='DB_HOST')
    db_port: str = Field(..., env='DB_PORT')
    db_database: str = Field(..., env='DB_NAME')
    db_username: str = Field(..., env='DB_USER')
    db_password: str = Field(..., env='DB_PASSWORD')

    # Настройки Logstash
    logstash_use: str = Field(..., env='LOGSTASH_USE')
    logstash_host: str = Field(..., env='LOGSTASH_HOST')
    logstash_port: int = Field(..., env='LOGSTASH_PORT')
    logstash_tags: str = Field(..., env='LOGSTASH_TAGS')

    # Общие настройки
    logger_name: str = Field(..., env='LOGGER_NAME')
    backoff_max_time: int = Field(..., env='BACKOFF_MAX_TIME')
    wait_timeout: int = Field(..., env='WAIT_TIMEOUT')
    main_process_sleep_time: int = Field(..., env='MAIN_PROCESS_SLEEP_TIME')

    class Config(object):
        """Класс настроек для родительского класса BaseSettings."""

        env_file = ENV_FILE_PATH
        json_loads = list_parse_fallback


settings = Settings()
