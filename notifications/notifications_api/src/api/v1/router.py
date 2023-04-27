"""Модуль для описания роутеров API конкретной версии."""
from api.v1 import events
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(events.router, prefix='/events', tags=['События'])
