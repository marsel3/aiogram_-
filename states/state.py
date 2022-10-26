from aiogram.dispatcher.filters.state import StatesGroup, State


class State(StatesGroup):
    category = State()

    count = State()
    new_count = State()

    tovar_id = State()

    search_tovar = State()