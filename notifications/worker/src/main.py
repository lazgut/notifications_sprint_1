"""Основной модуль. Точка входа в программу."""
import sys
from logging import config, getLogger

import logstash
from core.config import settings
from core.logger import LOGGING
from esb import base_esb
from services.worker import Worker

logger = getLogger(settings.logger_name)
config.dictConfig(LOGGING)
if settings.logstash_use:
    logger.addHandler(logstash.LogstashHandler(
        settings.logstash_host, settings.logstash_port, tags=settings.logstash_tags, version=1,
    ))

base_esb.esb = base_esb.RabbitMQ()

if len(sys.argv) > 1:
    queue = sys.argv[1].strip()
else:
    queue = 'email'

if __name__ == '__main__':
    Worker(esb=base_esb.esb, queue=queue).run()
