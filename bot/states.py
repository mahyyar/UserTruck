from aiogram.fsm.state import StatesGroup, State


class AddUserState(StatesGroup):
    panel = State()
    numeric_id = State()
    user_id = State()
    expire_day = State()
    confirm = State()


class EditUserState(StatesGroup):
    search_panel = State()
    choose_user = State()
    choose_field = State()
    new_value = State()
    confirm = State()


class DeleteUserState(StatesGroup):
    search_panel = State()
    choose_user = State()
    confirm = State()


class SearchState(StatesGroup):
    choose_method = State()
    search_username = State()
    search_numeric = State()
    search_panel = State()
    search_expire = State()

class NoteState(StatesGroup):
    editing = State()
