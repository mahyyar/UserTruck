
from aiogram import Router, F
from aiogram.types import CallbackQuery
from bot.cleaner import send_clean
from bot.keyboards import extend_buttons
from core.checker import due_today, due_tomorrow, overdue, days_left

router = Router()

@router.callback_query(F.data == "show_due")
async def show_due(call: CallbackQuery):
    t=due_today(); tm=due_tomorrow(); ov=overdue()
    text="🗂 تمدیدی‌ها:\n\n"
    text+="📅 امروز:\n" + "\n".join([f"{u[3]} | {u[4]}" for u in t]) + "\n\n"
    text+="⏳ فردا:\n" + "\n".join([f"{u[3]} | {u[4]}" for u in tm]) + "\n\n"
    text+="❗ عقب‌افتاده:\n"
    for u in ov:
        text+=f"{u[3]} | {u[4]} | تأخیر {abs(days_left(u[4]))} روز\n"
    await send_clean(call.bot, call.message.chat.id, text, reply_markup=extend_buttons(t+tm+ov))
