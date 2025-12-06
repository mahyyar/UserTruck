from aiogram import Bot

last_message = {}      
user_last_message = {} 


async def store_user(msg):
    user_last_message[msg.chat.id] = msg.message_id


async def send_clean(bot: Bot, chat_id: int, text: str, reply_markup=None):
    old_last = last_message.get(chat_id)
    old_user = user_last_message.get(chat_id)

    if old_last:
        try:
            await bot.delete_message(chat_id, old_last)
        except:
            pass

    if old_user:
        try:
            await bot.delete_message(chat_id, old_user)
        except:
            pass

    msg = await bot.send_message(chat_id, text, reply_markup=reply_markup)

    last_message[chat_id] = msg.message_id

    return msg
