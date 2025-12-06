from aiogram import Router, F
from aiogram.types import CallbackQuery
from bot.cleaner import send_clean
from core.checker import extend_next_month

router = Router()

@router.callback_query(F.data.startswith("extend:"))
async def extend(call: CallbackQuery):
    uid = int(call.data.split(":")[1])
    extend_next_month(uid)
    await send_clean(call.bot, call.message.chat.id, "تمدید انجام شد.")
