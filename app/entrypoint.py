from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from loguru import logger

from app.core import settings
from app.services.event_checker import event_checker


playlist_bot = Bot(token=settings.BOT_TOKEN)

storage = MemoryStorage()
dp = Dispatcher(playlist_bot, storage=storage)
scheduler = AsyncIOScheduler()


async def on_starup(dispatcher: Dispatcher, url=None, cert=None):  # noqa
    scheduler.add_job(event_checker, "interval", seconds=15, args=[dispatcher.bot])
    logger.info("РАБОТАЕТ")
