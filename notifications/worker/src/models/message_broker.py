"""Содержит описание событий в очереди брокера, которые нужны для работы процесса."""
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel


class Event(BaseModel):
    """Класс сообщения из очереди брокера."""

    template_id: UUID
    user_ids: Optional[list[UUID]]
    context: dict[str, Any]
