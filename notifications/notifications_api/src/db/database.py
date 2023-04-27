"""Модуль для подключения к СУБД через SQLAlchemy."""
from logging import getLogger
from typing import AsyncIterator

from core.config import settings
from sqlalchemy import URL
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

logger = getLogger(settings.logger_name)

url_object = URL.create(
    drivername=settings.db_drivername,
    username=settings.db_username,
    password=settings.db_password,
    host=settings.db_host,
    port=settings.db_port,
    database=settings.db_database,
)

async_engine = create_async_engine(url_object)
async_session = async_sessionmaker(async_engine)


async def get_db_session() -> AsyncIterator[async_sessionmaker]:
    """Получить сессию с СУБД.

    Yields:
        асинхронная сессия.
    """
    try:
        yield async_session
    except SQLAlchemyError as exception:
        logger.exception(exception)
    await async_engine.dispose()
