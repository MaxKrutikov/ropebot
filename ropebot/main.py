import asyncio
import logging

from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from ropebot.middlewares.middleware import BannedMiddlware
from ropebot.config.config import load_config
from ropebot.database.database import create_a_table
from ropebot.handlers.admin_handlers.admin_message import admin_router
from ropebot.handlers.god_handlers.god_message import god_router
from ropebot.handlers.player_handlers.player_message import player_router

async def main():

    config = load_config()
    logging.basicConfig(level=config.log_settings.log_level,
                        format=config.log_settings.log_format

    )

    redis = Redis(host='localhost')
    storage = RedisStorage(redis=redis)

    bot = Bot(token=config.telegrambot.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=storage)


    create_a_table()

    dp.include_router(god_router)
    dp.include_router(admin_router)
    dp.include_router(player_router)

    dp.message.outer_middleware(BannedMiddlware())

    task1 = asyncio.create_task(dp.start_polling(bot, players_dict=config.telegrambot.players_dict, admin_dict=config.telegrambot.admin_dict, god_dict=config.telegrambot.god_dict))
    task2 = asyncio.create_task(bot.delete_webhook(drop_pending_updates=True))

    await task1
    await task2

if __name__ == '__main__':
    asyncio.run(main())


