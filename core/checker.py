from datetime import datetime
from core.db import connect


def get_users():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    r = cur.fetchall()
    conn.close()
    return r


def due_today():
    t = datetime.now().day
    return [u for u in get_users() if u[4] == t]


def due_tomorrow():
    t = datetime.now().day + 1
    return [u for u in get_users() if u[4] == t]


def overdue():
    t = datetime.now().day
    return [u for u in get_users() if u[4] and u[4] < t]


def days_left(exp):
    t = datetime.now().day
    if exp >= t:
        return exp - t
    return (30 - t) + exp


def extend_next_month(uid):
    t = datetime.now().day
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE users SET expire_day=? WHERE id=?", (t, uid))
    conn.commit()
    conn.close()


def update_user(uid, field, value):
    conn = connect()
    cur = conn.cursor()
    cur.execute(f"UPDATE users SET {field}=? WHERE id=?", (value, uid))
    conn.commit()
    conn.close()


def delete_user(uid):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id=?", (uid,))
    conn.commit()
    conn.close()


def add_user(u, n, p, e):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (user_id,numeric_id,panel_name,expire_day) VALUES (?,?,?,?)",
        (u, n, p, e)
    )
    conn.commit()
    conn.close()


def search_by_panel(q):
    return [u for u in get_users() if q.lower() in u[3].lower()]


def get_user_by_id(uid):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id, user_id, numeric_id, panel_name, expire_day, last_extended FROM users WHERE id=?", (uid,))
    row = cur.fetchone()
    conn.close()
    return row


def extended_list():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id, user_id, numeric_id, panel_name, expire_day, last_extended FROM users WHERE last_extended IS NOT NULL ORDER BY last_extended DESC")
    rows = cur.fetchall()
    conn.close()
    return rows


def get_extended_users():
    return extended_list()


def get_all_users():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id, user_id, numeric_id, panel_name, expire_day, last_extended FROM users ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows


def count_due_today():
    return len(due_today())


def count_extended():
    return len(get_extended_users())


def count_overdue():
    return len(overdue())

def add_history(uid, text):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT history FROM users WHERE id=?", (uid,))
    h = cur.fetchone()
    old = h[0] if h and h[0] else ""

    now = datetime.now().strftime("%Y-%m-%d")
    new_line = f"[{now}] {text}\n"
    updated = old + new_line

    cur.execute("UPDATE users SET history=? WHERE id=?", (updated, uid))
    conn.commit()
    conn.close()

def get_history(uid):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT history FROM users WHERE id=?", (uid,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row and row[0] else "تاریخچه‌ای ثبت نشده است."


def users_expiring_in_days(days=5):
    today = datetime.now().day
    upcoming = []

    for u in get_users():
        exp_day = u[4]

        if exp_day is None:
            continue

        if exp_day >= today:
            diff = exp_day - today
        else:
            diff = (30 - today) + exp_day

        if 1 <= diff <= days:
            upcoming.append((u, diff))

    return upcoming
