from aiogram import Router, F
from aiogram.types import CallbackQuery
from bot.cleaner import send_clean
from core.checker import delete_user

router = Router()

@router.callback_query(F.data.startswith("delete_user:"))
async def remove(call: CallbackQuery):
    uid = int(call.data.split(":")[1])
    delete_user(uid)
    await send_clean(call.bot, call.message.chat.id, "کاربر حذف شد.")
