from aiogram.types import Message, ShippingOption, ShippingQuery, LabeledPrice, PreCheckoutQuery
from aiogram.types.message import ContentType
from aiogram.types import CallbackQuery

from data.config import PAYMENT_TOKEN
from loader import dp

PRICES = [
    LabeledPrice(label='Ноутбук', amount=1000),
    LabeledPrice(label='Прочная упаковка', amount=1000)
]

SUPERSPEED_SHIPPING_OPTION = ShippingOption(
    id='superspeed',
    title='Супер быстрая!'
).add(LabeledPrice('Лично в руки!', 1000))

POST_SHIPPING_OPTION = ShippingOption(
    id='post',
    title='Почта России'
)

POST_SHIPPING_OPTION.add(LabeledPrice('Кортонная коробка', 1000))
POST_SHIPPING_OPTION.add(LabeledPrice('Срочное отправление!', 1000))

PICKUP_SHIPPING_OPTION = ShippingOption(
    id='pickup',
    title='Самовывоз'
)
PICKUP_SHIPPING_OPTION.add(LabeledPrice('Самовывоз в Сантк-Петербурге', 1000))

@dp.callback_query_handler(text='pay')
async def buy_process(call: CallbackQuery):
    await dp.bot.delete_message(call.message.chat.id, call.message.message_id)
    await dp.bot.send_invoice(
    chat_id = call.message.chat.id,
        title='Оформить заказ',
        description='самовывоз',
        provider_token=PAYMENT_TOKEN,
        currency='RUB',
        need_email=True,
        need_phone_number=True,
        is_flexible=True,
        prices=[LabeledPrice("Шрек", 29000)],
        start_parameter='example',
        payload='some_invoice')


@dp.shipping_query_handler(lambda q: True)
async def shipping_process(shipping_query: ShippingQuery):
    if shipping_query.shipping_address.country_code == 'AU':
        return await dp.bot.answer_shipping_query(
            shipping_query.id,
            ok=False,
            error_message='AU_error'
        )

    shipping_options = [SUPERSPEED_SHIPPING_OPTION]

    if shipping_query.shipping_address.country_code == 'RU':
        shipping_options.append(POST_SHIPPING_OPTION)

        if shipping_query.shipping_address.city == 'Санкт-Петербург':
            shipping_options.append(PICKUP_SHIPPING_OPTION)

    await dp.bot.answer_shipping_query(
        shipping_query.id,
        ok=True,
        shipping_options=shipping_options
    )

@dp.pre_checkout_query_handler(lambda q: True)
async def checkout_process(pre_checkout_query: PreCheckoutQuery):
    await dp.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message):
    await dp.bot.send_message(
        message.chat.id,
        'successful_payment'
    )