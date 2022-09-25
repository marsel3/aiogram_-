from aiogram.types import Message, ShippingOption, ShippingQuery, LabeledPrice, PreCheckoutQuery
from aiogram.types.message import ContentType
from aiogram.types import CallbackQuery
from data.config import admins_id

from loader import db_tovars, db_users
from data.config import PAYMENT_TOKEN
from loader import dp, db_users


SUPERSPEED_SHIPPING_OPTION = ShippingOption(
    id='city_delivery',
    title='Доставка по городу!'
).add(LabeledPrice('Лично в руки!', 20000))

POST_SHIPPING_OPTION = ShippingOption(
    id='post',
    title='Почта России'
)
POST_SHIPPING_OPTION.add(LabeledPrice('Картонная коробка', 1700))
POST_SHIPPING_OPTION.add(LabeledPrice('Срочное отправление!', 2500))
POST_SHIPPING_OPTION.add(LabeledPrice('Кортонная коробка', 1000))
POST_SHIPPING_OPTION.add(LabeledPrice('Срочное отправление!', 1000))

PICKUP_SHIPPING_OPTION = ShippingOption(
    id='pickup',
    title='Самовывоз'
)
PICKUP_SHIPPING_OPTION.add(LabeledPrice('Самовывоз в Казани', 1000))


@dp.callback_query_handler(text='pay')
async def buy_process(call: CallbackQuery):
    PRICES = []
    for i in db_users.basket_list(call.from_user.id):
        PRICES.append(LabeledPrice(i[1], int(i[2] * i[3] * 100)))
    await dp.bot.delete_message(call.message.chat.id, call.message.message_id)
    #try:
    await dp.bot.send_invoice(
        chat_id=call.message.chat.id,
        title='Заказ № ???',
        description='самовывоз',
        provider_token=PAYMENT_TOKEN,
        currency='RUB',
        need_email=True,
        need_phone_number=True,
        is_flexible=True,
        prices=PRICES,
        start_parameter='example',
        payload='some_invoice')
    #except:
        #await dp.bot.send_message(chat_id = call.message.chat.id,
                                  #text='Минимальная сумма заказа 1$')


@dp.shipping_query_handler(lambda q: True)
async def shipping_process(shipping_query: ShippingQuery):
    if shipping_query.shipping_address.country_code == 'AU':
        return await dp.bot.answer_shipping_query(
            shipping_query.id,
            ok=False,
            error_message='AU_error'
        )

    shipping_options = []
    if shipping_query.shipping_address.city.title() == 'Казань':
        shipping_options.append(PICKUP_SHIPPING_OPTION)
        shipping_options.append(SUPERSPEED_SHIPPING_OPTION)
    elif shipping_query.shipping_address.country_code == 'RU':
        shipping_options.append(POST_SHIPPING_OPTION)


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
        'Заказ оплачен, и уже начал собираться)'
    )
    print(message.successful_payment)
    user_name = db_users.user_fullname(message.from_user.id)

    pmnt = message.successful_payment.to_python()
    for key, val in pmnt.items():
        print(f'{key} = {val}')

    for admin in admins_id:
        try:
            text = f'Пользователь {user_name} оплатил заказ на сумму {message.successful_payment.total_amount / 100}₽' \
                   f'\n\nДанные пользователя: ' \
                   f'\nНомер телефона: {message.successful_payment.order_info.phone_number}' \
                   f'\nemail: \t{message.successful_payment.order_info.email}' \
                   f'\nАдрес заказа: г. {message.successful_payment.order_info.shipping_address.city} ул. {message.successful_payment.order_info.shipping_address.street_line1}, {message.successful_payment.order_info.shipping_address.street_line2}' \
                   f'\nСпособ доставки: {message.successful_payment.shipping_option_id}'

            await dp.bot.send_message(chat_id=admin, text=text)
        except Exception as err:
            print('иди нахуй!!!')