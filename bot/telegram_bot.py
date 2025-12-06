import asyncio
from aiogram import Bot, Dispatcher
from config.settings import BOT_TOKEN

from bot.handlers.start import router as r_start
from bot.handlers.main_menu import router as r_main
from bot.handlers.stats import router as r_stats
from bot.handlers.due import router as r_due
from bot.handlers.extend import router as r_extend
from bot.handlers.add_user import router as r_add
from bot.handlers.edit_user import router as r_edit
from bot.handlers.delete_user import router as r_delete
from bot.handlers.search_user import router as r_search

from core.db import init_db, optimize_db
from bot.handlers.renew_auto import send_renewal_notifications
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import pytz

bot = Bot(BOT_TOKEN)
init_db()
optimize_db()
dp = Dispatcher()

def register_all_handlers():
    dp.include_router(r_main)
    dp.include_router(r_stats)
    dp.include_router(r_due)
    dp.include_router(r_extend)
    dp.include_router(r_add)
    dp.include_router(r_edit)
    dp.include_router(r_delete)
    dp.include_router(r_search)
    dp.include_router(r_start)

async def _run():
    register_all_handlers()

    scheduler = AsyncIOScheduler(timezone=pytz.timezone("Asia/Tehran"))
    scheduler.add_job(
        send_renewal_notifications,
        "cron",
        hour=12,
        minute=0,
        args=[bot]
    )
    scheduler.start()

    await dp.start_polling(bot)

def start_bot():
    asyncio.run(_run())
