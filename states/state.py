from aiogram.dispatcher.filters.state import StatesGroup, State


class Search(StatesGroup):
    tovar_name = State()


class SetCount(StatesGroup):
    msg_list = State()
    tovar_id = State()
    count = State()


class SetCountInBasket(StatesGroup):
    msg_list = State()
    tovar_id = State()
    count = State()



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
