import asyncio

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from bot.clients.Chat_GPT import AIAgent
from bot.clients.db import DBClient
from bot.handlers.common import common_router
from bot.log import logger
from config import Config


async def main():
    # db init
    db_client = DBClient(db_url=Config.POSTGRES_DSN)

    # ai_assistant init
    ai_assistant = AIAgent()

    # bot init
    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(
        token=Config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    bot.db = db_client
    bot.ai = ai_assistant

    # include routers
    dp.include_router(common_router)

    # bot start
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Bot is starting!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
