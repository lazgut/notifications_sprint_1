"""Основной модуль приложения. Точка входа в приложение."""
from logging import DEBUG, config, getLogger

import logstash
import uvicorn
from api.v1.router import api_router
from core.config import settings
from core.logger import LOGGING
from esb import base_esb
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

logger = getLogger(settings.logger_name)
config.dictConfig(LOGGING)
if settings.logstash_use:
    logger.addHandler(logstash.LogstashHandler(
        settings.logstash_host, settings.logstash_port, tags=settings.logstash_tags, version=1,
    ))


app = FastAPI(
    title=settings.project_name,
    description=settings.project_descr,
    docs_url='/api/v1',
    openapi_url='/api/v1/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    """Событие запуска FastAPI."""
    logger.info('Notification service started')

    base_esb.esb = base_esb.RabbitMQ()
    await base_esb.esb.connect()


@app.on_event('shutdown')
async def shutdown_event():
    """Событие остановки FastAPI."""
    await base_esb.esb.disconnect()
    logger.info('Notification service stopped')

app.include_router(api_router, prefix='/api/v1')


if __name__ == '__main__':
    uvicorn.run(
        app=settings.uvicorn_app_name,
        host=settings.uvicorn_host,
        port=settings.uvicorn_port,
        log_config=LOGGING,
        log_level=DEBUG,
    )
