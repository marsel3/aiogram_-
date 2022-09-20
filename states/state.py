from aiogram.dispatcher.filters.state import StatesGroup, State


class State(StatesGroup):
    category = State()

    count = State()
