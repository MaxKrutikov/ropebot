from aiogram import BaseMiddleware
from typing import Callable, Any, Awaitable
from aiogram.types import TelegramObject

class BannedMiddlware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any],
    ) -> Any:

        if any([data['event_context'].chat.id in data['god_dict'].values(), data['event_context'].chat.id in data['players_dict'].values(), data['event_context'].chat.id in data['admin_dict'].values()]):
            result = await handler(event, data)
        else:
            return

