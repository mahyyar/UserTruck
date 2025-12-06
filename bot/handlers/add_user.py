from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from bot.states import AddUserState
from bot.cleaner import send_clean, store_user
from core.checker import add_user
from bot.keyboards import back_button

router = Router()

@router.callback_query(F.data == "add_user")
async def start_add(call: CallbackQuery, state: FSMContext):
    await state.set_state(AddUserState.panel)
    await send_clean(call.bot, call.message.chat.id, "نام پنل را وارد کنید:", reply_markup=back_button())

@router.message(AddUserState.panel)
async def step1(msg: Message, state: FSMContext):
    if msg.text == "↩ بازگشت":
        await state.clear()
        await send_clean(msg.bot, msg.chat.id, "بازگشت.", reply_markup=back_button())
        return

    await store_user(msg)
    await state.update_data(panel=msg.text)
    await state.set_state(AddUserState.numeric_id)
    await send_clean(msg.bot, msg.chat.id, "آیدی عددی را وارد کنید:", reply_markup=back_button())

@router.message(AddUserState.numeric_id)
async def step2(msg: Message, state: FSMContext):
    if msg.text == "↩ بازگشت":
        await state.set_state(AddUserState.panel)
        await send_clean(msg.bot, msg.chat.id, "نام پنل را وارد کنید:", reply_markup=back_button())
        return

    if not msg.text.isdigit():
        await send_clean(msg.bot, msg.chat.id, "آیدی عددی باید فقط عدد باشد.", reply_markup=back_button())
        return

    await store_user(msg)
    await state.update_data(numeric_id=msg.text)
    await state.set_state(AddUserState.user_id)
    await send_clean(msg.bot, msg.chat.id, "یوزرنیم تلگرام را وارد کنید (شروع با @):", reply_markup=back_button())

@router.message(AddUserState.user_id)
async def step3(msg: Message, state: FSMContext):
    if msg.text == "↩ بازگشت":
        await state.set_state(AddUserState.numeric_id)
        await send_clean(msg.bot, msg.chat.id, "آیدی عددی را وارد کنید:", reply_markup=back_button())
        return

    username = msg.text.strip()

    if not username.startswith("@"):
        await send_clean(msg.bot, msg.chat.id, "یوزرنیم باید با @ شروع شود.", reply_markup=back_button())
        return

    if not username[1:].isalnum():
        await send_clean(msg.bot, msg.chat.id, "یوزرنیم باید انگلیسی و بدون فاصله باشد.", reply_markup=back_button())
        return

    await store_user(msg)
    await state.update_data(user_id=username)
    await state.set_state(AddUserState.expire_day)
    await send_clean(msg.bot, msg.chat.id, "روز تمدید را وارد کنید (عدد کمتر از ۳۰):", reply_markup=back_button())

@router.message(AddUserState.expire_day)
async def step4(msg: Message, state: FSMContext):
    if msg.text == "↩ بازگشت":
        await state.set_state(AddUserState.user_id)
        await send_clean(msg.bot, msg.chat.id, "یوزرنیم تلگرام را وارد کنید:", reply_markup=back_button())
        return

    if not msg.text.isdigit():
        await send_clean(msg.bot, msg.chat.id, "روز تمدید باید عدد باشد.", reply_markup=back_button())
        return

    day = int(msg.text)

    if day <= 0 or day >= 31:
        await send_clean(msg.bot, msg.chat.id, "روز تمدید باید بین 1 تا 29 باشد.", reply_markup=back_button())
        return

    await store_user(msg)
    data = await state.get_data()
    add_user(data["user_id"], data["numeric_id"], data["panel"], day)

    await send_clean(msg.bot, msg.chat.id, "کاربر با موفقیت اضافه شد.", reply_markup=back_button())
    await state.clear()
