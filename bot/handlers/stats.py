from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.cleaner import send_clean
from bot.keyboards import back_button, pagination_buttons
from core.checker import (
    get_extended_users,
    get_all_users,
    users_expiring_in_days,
    due_today,
    due_tomorrow,
    overdue,
    extended_list
)
import math

router = Router()

ITEMS_PER_PAGE = 20


@router.callback_query(F.data == "stats")
async def show_stats_menu(call: CallbackQuery):
    from bot.keyboards import stats_menu
    await send_clean(call.bot, call.message.chat.id, "منوی آمار:", reply_markup=stats_menu())


@router.callback_query(F.data == "advanced_stats")
async def show_advanced_stats(call: CallbackQuery):
    total = len(get_all_users())
    extended = len(extended_list())
    today = len(due_today())
    tomorrow = len(due_tomorrow())
    over = len(overdue())
    near = len(users_expiring_in_days(5))

    text = (
        "📊 آمار حرفه‌ای:\n\n"
        f"👥 تعداد کل کاربران: {total}\n"
        f"📘 تعداد تمدید شده‌ها: {extended}\n"
        f"📅 تمدید امروز: {today}\n"
        f"⏳ تمدید فردا: {tomorrow}\n"
        f"⚠️ عقب‌افتاده‌ها: {over}\n"
        f"🔔 نزدیک تمدید (۵ روز آینده): {near}\n"
    )

    await send_clean(call.bot, call.message.chat.id, text, reply_markup=back_button())

async def show_page(call, state: FSMContext):
    data = await state.get_data()

    list_type = data.get("list_type")
    page = data.get("page", 1)

    if list_type == "extended":
        users = get_extended_users()
        title = "📘 لیست تمدید شده‌ها:"
        formatter = lambda u: f"- {u[3]} | آیدی عددی {u[2]}\n"

    elif list_type == "all_users":
        users = get_all_users()
        title = "📋 لیست کاربران:\n\n"
        formatter = lambda u: (
            f"👤 user = {u[1]}\n"
            f"🆔 id = {u[2]}\n"
            f"🎫 panel = {u[3]}\n"
            f"📅 renew = {u[4]}\n"
            "──────────────\n"
        )

    elif list_type == "near_expire":
        raw = users_expiring_in_days(5)
        users = [(u, diff) for u, diff in raw]
        title = "🔔 نزدیک تمدید (۵ روز آینده):\n\n"
        formatter = lambda row: f"{row[1]} روز مانده → {row[0][1]} | id {row[0][2]} | panel {row[0][3]}\n"

    else:
        await send_clean(call.bot, call.message.chat.id, "خطا: وضعیت نامشخص.", reply_markup=back_button())
        return

    total_pages = max(1, math.ceil(len(users) / ITEMS_PER_PAGE))

    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages

    await state.update_data(page=page)

    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    chunk = users[start:end]

    text = title + "\n"
    for user in chunk:
        text += formatter(user)

    await send_clean(
        call.bot,
        call.message.chat.id,
        text,
        reply_markup=pagination_buttons(page, total_pages)
    )

@router.callback_query(F.data == "stat_extended")
async def stat_extended(call: CallbackQuery, state: FSMContext):
    users = get_extended_users()
    if not users:
        await send_clean(call.bot, call.message.chat.id, "هیچ کاربری تمدید نشده است.", reply_markup=back_button())
        return

    await state.update_data(list_type="extended", page=1)
    await show_page(call, state)


@router.callback_query(F.data == "stat_all_users")
async def stat_all_users(call: CallbackQuery, state: FSMContext):
    users = get_all_users()
    if not users:
        await send_clean(call.bot, call.message.chat.id, "هیچ کاربری ثبت نشده است.", reply_markup=back_button())
        return

    await state.update_data(list_type="all_users", page=1)
    await show_page(call, state)


@router.callback_query(F.data == "near_expire")
async def near_expire(call: CallbackQuery, state: FSMContext):
    users = users_expiring_in_days(5)
    if not users:
        await send_clean(call.bot, call.message.chat.id, "هیچ کاربری در ۵ روز آینده تمدید ندارد.", reply_markup=back_button())
        return

    await state.update_data(list_type="near_expire", page=1)
    await show_page(call, state)


@router.callback_query(F.data.startswith("page_prev:"))
async def prev_page(call: CallbackQuery, state: FSMContext):
    page = int(call.data.split(":")[1]) - 1
    await state.update_data(page=page)
    await show_page(call, state)


@router.callback_query(F.data.startswith("page_next:"))
async def next_page(call: CallbackQuery, state: FSMContext):
    page = int(call.data.split(":")[1]) + 1
    await state.update_data(page=page)
    await show_page(call, state)
