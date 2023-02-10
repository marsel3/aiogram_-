from aiogram.dispatcher.filters.state import StatesGroup, State


class State1(StatesGroup):
    category = State()

    count = State()
    new_count = State()

    tovar_id = State()

    search_tovar = State()


class FSMAdmin(StatesGroup):
    category_id = State()

    tovar_name = State()
    tovar_price = State()
    tovar_disc = State()
    tovar_photo = State()

    agreement = State()


class FSMAdminEdit(StatesGroup):
    category_id = State()

    tovar_name = State()
    tovar_price = State()
    tovar_disc = State()
    tovar_photo = State()
