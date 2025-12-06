from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from bot.states import EditUserState
from bot.cleaner import send_clean, store_user
from core.checker import update_user, get_user_by_id
from bot.keyboards import back_button

router = Router()

@router.callback_query(F.data.startswith("edit_panel:"))
async def ask_panel(call: CallbackQuery, state: FSMContext):
    uid = int(call.data.split(":")[1])
    await state.set_state(EditUserState.new_value)
    await state.update_data(uid=uid, field="panel_name")
    await send_clean(call.bot, call.message.chat.id, "نام جدید پنل را وارد کنید:", reply_markup=back_button())

@router.callback_query(F.data.startswith("edit_numeric:"))
async def ask_numeric(call: CallbackQuery, state: FSMContext):
    uid = int(call.data.split(":")[1])
    await state.set_state(EditUserState.new_value)
    await state.update_data(uid=uid, field="numeric_id")
    await send_clean(call.bot, call.message.chat.id, "آیدی عددی جدید را وارد کنید:", reply_markup=back_button())

@router.callback_query(F.data.startswith("edit_expire:"))
async def ask_expire(call: CallbackQuery, state: FSMContext):
    uid = int(call.data.split(":")[1])
    await state.set_state(EditUserState.new_value)
    await state.update_data(uid=uid, field="expire_day")
    await send_clean(call.bot, call.message.chat.id, "روز تمدید جدید را وارد کنید:", reply_markup=back_button())

@router.message(EditUserState.new_value)
async def apply_edit(msg: Message, state: FSMContext):
    if msg.text == "↩ بازگشت":
        await state.clear()
        await send_clean(msg.bot, msg.chat.id, "بازگشت.", reply_markup=back_button())
        return

    await store_user(msg)
    data = await state.get_data()
    uid = data["uid"]
    field = data["field"]
    value = msg.text

    if field == "expire_day":
        try:
            value = int(value)
        except:
            await send_clean(msg.bot, msg.chat.id, "روز نامعتبر است.", reply_markup=back_button())
            return

    update_user(uid, field, value)
    await state.clear()

    await send_clean(msg.bot, msg.chat.id, "اطلاعات بروزرسانی شد.", reply_markup=back_button())
