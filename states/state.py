from aiogram.dispatcher.filters.state import StatesGroup, State


class ConfirmOrder(StatesGroup):
    msg_list = State()
    callback = State()

    fio = State()
    phone = State()


class AdminSpam(StatesGroup):
    msg_list = State()
    text = State()
    confirm = State()


class Search(StatesGroup):
    msg_list = State()
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
    msg_list = State()
    callback = State()

    category_id = State()
    category = State()

    product = State()
    product_price = State()
    product_desc = State()
    product_photo = State()
    product_rating = State()

    agreement = State()


class FSMAdminDelete(StatesGroup):
    msg_list = State()
    callback = State()

    category_id = State()
    category = State()

    product_id = State()
    product = State()


class FSMAdminEdit(StatesGroup):
    msg_list = State()
    callback = State()

    product_id = State()
    category_id = State()
    category = State()

    product = State()
    product_price = State()
    product_desc = State()
    product_photo = State()
    product_rating = State()

    agreement = State()