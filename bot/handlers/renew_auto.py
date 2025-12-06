from aiogram import Bot
from core.checker import due_today, due_tomorrow, overdue
from config.settings import ADMIN_ID


async def send_renewal_notifications(bot: Bot):
    users_today = due_today()
    users_tomorrow = due_tomorrow()
    users_overdue = overdue()

    text = "📊 گزارش روزانه تمدیدها:\n\n"

    text += "📅 تمدید امروز:\n"
    if users_today:
        for u in users_today:
            text += f"- {u[1]} | panel {u[3]} | id {u[2]}\n"
    else:
        text += "هیچ موردی وجود ندارد.\n"

    text += "\n📅 تمدید فردا:\n"
    if users_tomorrow:
        for u in users_tomorrow:
            text += f"- {u[1]} | panel {u[3]} | id {u[2]}\n"
    else:
        text += "هیچ موردی وجود ندارد.\n"

    text += "\n⚠️ عقب‌افتاده:\n"
    if users_overdue:
        for u in users_overdue:
            text += f"- {u[1]} | panel {u[3]} | id {u[2]}\n"
    else:
        text += "هیچ موردی وجود ندارد.\n"

    try:
        await bot.send_message(ADMIN_ID, text)
    except:
        pass
