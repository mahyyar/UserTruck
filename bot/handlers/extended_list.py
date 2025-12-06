from aiogram import Router, F
from aiogram.types import CallbackQuery
from bot.cleaner import send_clean
from bot.keyboards import extended_menu
from core.checker import extended_list

router = Router()

@router.callback_query(F.data == "extended_list")
async def show_extended(call: CallbackQuery):
    users = extended_list()

    if not users:
        await send_clean(call.bot, call.message.chat.id, "هنوز هیچ کاربری تمدید نشده است.")
        return

    await send_clean(
        call.bot,
        call.message.chat.id,
        "📘 لیست تمدید شده‌ها:",
        reply_markup=extended_menu(users)
    )
