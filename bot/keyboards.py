from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🗂 نمایش تمدیدی‌ها", callback_data="show_due")],
        [InlineKeyboardButton(text="📊 آمار", callback_data="stats")],
        [InlineKeyboardButton(text="🔧 پنل مدیریت", callback_data="panel")]
    ])

def stats_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📘 لیست تمدید شده‌ها", callback_data="stat_extended")],
        [InlineKeyboardButton(text="📋 لیست تمام کاربران", callback_data="stat_all_users")],
        [InlineKeyboardButton(text="📊 آمار حرفه‌ای", callback_data="advanced_stats")],
        [InlineKeyboardButton(text="🔔 نزدیک تمدید", callback_data="near_expire")],
        [InlineKeyboardButton(text="↩ بازگشت", callback_data="back")]
    ])

def panel_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ افزودن کاربر", callback_data="add_user")],
        [InlineKeyboardButton(text="🔍 جستجو", callback_data="search_user")],
        [InlineKeyboardButton(text="↩ بازگشت", callback_data="back")]
    ])



def extend_buttons(users):
    rows = []
    for u in users:
        rows.append([
            InlineKeyboardButton(
                text=f"✔ تمدید {u[3]}",
                callback_data=f"extend:{u[0]}"
            )
        ])
    rows.append([InlineKeyboardButton(text="↩ بازگشت", callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def extended_menu(users):
    rows = []
    for u in users:
        rows.append([
            InlineKeyboardButton(
                text=f"{u[3]} (تمدید شده)",
                callback_data=f"manage_user:{u[0]}"
            )
        ])
    rows.append([InlineKeyboardButton(text="↩ بازگشت", callback_data="panel")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def search_results(users):
    rows = []
    for u in users:
        rows.append([
            InlineKeyboardButton(
                text=f"{u[3]} | {u[2]}",
                callback_data=f"manage_user:{u[0]}"
            )
        ])
    rows.append([InlineKeyboardButton(text="↩ بازگشت", callback_data="panel")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

def manage_user_menu(uid):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🗑 حذف", callback_data=f"delete_user:{uid}")],
        [InlineKeyboardButton(text="✏ تغییر نام پنل", callback_data=f"edit_panel:{uid}")],
        [InlineKeyboardButton(text="🔢 تغییر آیدی عددی", callback_data=f"edit_numeric:{uid}")],
        [InlineKeyboardButton(text="📅 تغییر روز تمدید", callback_data=f"edit_expire:{uid}")],
        [InlineKeyboardButton(text="📝 یادداشت", callback_data=f"note:{uid}")],
        [InlineKeyboardButton(text="📜 تاریخچه", callback_data=f"history:{uid}")],
        [InlineKeyboardButton(text="↩ بازگشت", callback_data="panel")]
    ])

def back_button():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="↩ بازگشت", callback_data="back")]
    ])

def pagination_buttons(page, total_pages):
    buttons = []

    prev_btn = InlineKeyboardButton(text="⬅ قبلی", callback_data=f"page_prev:{page}")
    next_btn = InlineKeyboardButton(text="بعدی ➡", callback_data=f"page_next:{page}")

    row = []
    if page > 1:
        row.append(prev_btn)
    row.append(InlineKeyboardButton(text=f"{page}/{total_pages}", callback_data="no_action"))
    if page < total_pages:
        row.append(next_btn)

    buttons.append(row)
    buttons.append([InlineKeyboardButton(text="↩ بازگشت", callback_data="back")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def search_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1️⃣ جستجو با یوزرنیم", callback_data="search_username")],
        [InlineKeyboardButton(text="2️⃣ جستجو با آیدی عددی", callback_data="search_numeric")],
        [InlineKeyboardButton(text="3️⃣ جستجو با نام پنل", callback_data="search_panel")],
        [InlineKeyboardButton(text="4️⃣ جستجو با روز تمدید", callback_data="search_expire")],
        [InlineKeyboardButton(text="↩ بازگشت", callback_data="back")]
    ])
