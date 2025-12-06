from aiogram import Router, F
from aiogram.types import CallbackQuery
from bot.keyboards import main_menu, panel_menu
from bot.cleaner import send_clean

router = Router()

@router.callback_query(F.data == "panel")
async def panel(call: CallbackQuery):
    await send_clean(call.bot, call.message.chat.id, "پنل مدیریت:", reply_markup=panel_menu())

@router.callback_query(F.data == "back")
async def back(call: CallbackQuery):
    await send_clean(call.bot, call.message.chat.id, "منوی اصلی:", reply_markup=main_menu())
