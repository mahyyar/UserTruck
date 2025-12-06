from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from bot.states import SearchState, NoteState
from bot.cleaner import send_clean, store_user
from bot.keyboards import search_menu, back_button, manage_user_menu

from core.checker import (
    search_by_panel,
    get_users,
    get_history,
    get_user_by_id,
    update_user,
    add_history
)

router = Router()


def format_user(u):
    return (
        "اطلاعات کاربر:\n\n"
        f"🆔 آیدی کاربر: {u[0]}\n"
        f"🔢 آیدی عددی: {u[2]}\n"
        f"🎫 نام پنل: {u[3]}\n"
        f"📅 روز تمدید: {u[4]}"
    )


@router.callback_query(F.data == "search_user")
async def start_search(call: CallbackQuery, state: FSMContext):
    await state.set_state(SearchState.choose_method)
    await send_clean(
        call.bot,
        call.message.chat.id,
        "🔍 روش جستجو را انتخاب کنید:\n\n"
        "1️⃣ با یوزرنیم\n"
        "2️⃣ با آیدی عددی\n"
        "3️⃣ با نام پنل\n"
        "4️⃣ با روز تمدید",
        reply_markup=search_menu()
    )

@router.callback_query(F.data == "search_username")
async def ask_username(call: CallbackQuery, state: FSMContext):
    await state.set_state(SearchState.search_username)
    await send_clean(call.bot, call.message.chat.id, "یوزرنیم را وارد کنید:", reply_markup=back_button())


@router.message(SearchState.search_username)
async def do_username_search(msg: Message, state: FSMContext):
    if msg.text == "↩ بازگشت":
        await start_search(msg, state)
        return

    username = msg.text.strip()
    if not username.startswith("@"):
        username = "@" + username

    if not username[1:].isalnum():
        await send_clean(msg.bot, msg.chat.id, "یوزرنیم باید انگلیسی باشد.", reply_markup=back_button())
        return

    users = [u for u in get_users() if u[1].lower() == username.lower()]

    if not users:
        await send_clean(msg.bot, msg.chat.id, "هیچ کاربری یافت نشد.", reply_markup=back_button())
        return

    for u in users:
        await send_clean(
            msg.bot,
            msg.chat.id,
            format_user(u),
            reply_markup=manage_user_menu(u[0])
        )

    await state.clear()

@router.callback_query(F.data == "search_numeric")
async def ask_numeric(call: CallbackQuery, state: FSMContext):
    await state.set_state(SearchState.search_numeric)
    await send_clean(call.bot, call.message.chat.id, "آیدی عددی را وارد کنید:", reply_markup=back_button())


@router.message(SearchState.search_numeric)
async def do_numeric_search(msg: Message, state: FSMContext):
    if msg.text == "↩ بازگشت":
        await start_search(msg, state)
        return

    if not msg.text.isdigit():
        await send_clean(msg.bot, msg.chat.id, "آیدی عددی باید عدد باشد.", reply_markup=back_button())
        return

    users = [u for u in get_users() if str(u[2]) == msg.text.strip()]

    if not users:
        await send_clean(msg.bot, msg.chat.id, "هیچ کاربری یافت نشد.", reply_markup=back_button())
        return

    for u in users:
        await send_clean(
            msg.bot,
            msg.chat.id,
            format_user(u),
            reply_markup=manage_user_menu(u[0])
        )

    await state.clear()

@router.callback_query(F.data == "search_panel")
async def ask_panel(call: CallbackQuery, state: FSMContext):
    await state.set_state(SearchState.search_panel)
    await send_clean(call.bot, call.message.chat.id, "نام پنل را وارد کنید:", reply_markup=back_button())


@router.message(SearchState.search_panel)
async def do_panel_search(msg: Message, state: FSMContext):
    if msg.text == "↩ بازگشت":
        await start_search(msg, state)
        return

    users = search_by_panel(msg.text)

    if not users:
        await send_clean(msg.bot, msg.chat.id, "هیچ کاربری یافت نشد.", reply_markup=back_button())
        return

    for u in users:
        await send_clean(
            msg.bot,
            msg.chat.id,
            format_user(u),
            reply_markup=manage_user_menu(u[0])
        )

    await state.clear()

@router.callback_query(F.data == "search_expire")
async def ask_expire(call: CallbackQuery, state: FSMContext):
    await state.set_state(SearchState.search_expire)
    await send_clean(call.bot, call.message.chat.id, "روز تمدید را وارد کنید:", reply_markup=back_button())


@router.message(SearchState.search_expire)
async def do_expire_search(msg: Message, state: FSMContext):
    if msg.text == "↩ بازگشت":
        await start_search(msg, state)
        return

    if not msg.text.isdigit():
        await send_clean(msg.bot, msg.chat.id, "عدد معتبر نیست.", reply_markup=back_button())
        return

    day = int(msg.text)
    if not 1 <= day <= 29:
        await send_clean(msg.bot, msg.chat.id, "روز تمدید باید بین 1 تا 29 باشد.", reply_markup=back_button())
        return

    users = [u for u in get_users() if u[4] == day]

    if not users:
        await send_clean(msg.bot, msg.chat.id, "هیچ کاربری یافت نشد.", reply_markup=back_button())
        return

    for u in users:
        await send_clean(
            msg.bot,
            msg.chat.id,
            format_user(u),
            reply_markup=manage_user_menu(u[0])
        )

    await state.clear()

@router.callback_query(F.data.startswith("history:"))
async def show_history(call: CallbackQuery):
    uid = int(call.data.split(":")[1])
    history = get_history(uid)

    await send_clean(
        call.bot,
        call.message.chat.id,
        "📜 تاریخچه کاربر:\n\n" + history,
        reply_markup=back_button()
    )

@router.callback_query(F.data.startswith("note:"))
async def note_menu(call: CallbackQuery, state: FSMContext):
    uid = int(call.data.split(":")[1])
    data = get_user_by_id(uid)

    note = data[6] if len(data) >= 7 and data[6] else "یادداشتی ثبت نشده است."

    await state.set_state(NoteState.editing)
    await state.update_data(uid=uid)

    await send_clean(
        call.bot,
        call.message.chat.id,
        f"📝 یادداشت کاربر:\n\n{note}\n\nبرای تغییر، متن جدید را ارسال کنید:",
        reply_markup=back_button()
    )


@router.message(NoteState.editing)
async def save_note(msg: Message, state: FSMContext):
    if msg.text == "↩ بازگشت":
        await state.clear()
        await send_clean(msg.bot, msg.chat.id, "بازگشت.", reply_markup=back_button())
        return

    data = await state.get_data()
    uid = data["uid"]

    update_user(uid, "note", msg.text)
    add_history(uid, "یادداشت تغییر کرد")

    await send_clean(msg.bot, msg.chat.id, "یادداشت ذخیره شد.", reply_markup=back_button())
    await state.clear()
