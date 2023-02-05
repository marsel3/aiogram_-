from aiogram.dispatcher.filters.state import StatesGroup, State


class State1(StatesGroup):
    category = State()

    count = State()
    new_count = State()

    tovar_id = State()

    search_tovar = State()

    category_add = State()
    category_edit = State()
    tovar_name = State()
    tovar_price = State()
    tovar_disc = State()