from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from bot.keyboards import main_menu
from bot.cleaner import send_clean

router = Router()

@router.message(CommandStart())
async def start_handler(msg: Message):
    await send_clean(msg.bot, msg.chat.id, "به ربات مدیریت تمدید خوش آمدید.", reply_markup=main_menu())
