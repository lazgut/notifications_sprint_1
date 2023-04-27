"""Основной модуль. Точка входа в программу."""
from logging import config, getLogger

import logstash
from core.config import settings
from core.logger import LOGGING
from scheduler import Scheduler

logger = getLogger(settings.logger_name)
config.dictConfig(LOGGING)
if settings.logstash_use:
    logger.addHandler(logstash.LogstashHandler(
        settings.logstash_host, settings.logstash_port, tags=settings.logstash_tags, version=1,
    ))

if __name__ == '__main__':
    Scheduler().run()
