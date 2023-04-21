import logging

from aiogram import Dispatcher

from data.config import admins_id


async def on_startup_notify(dp):
    for admin in admins_id:
        try:
            text = 'Бот запущен'
            await dp.bot.send_message(chat_id=admin, text=text)

        except Exception as err:
            logging.exception(err)


async def successful_payment(dp: Dispatcher, user_name, message):
    for admin in admins_id:
        print("Приетик =)")
        try:
            text = f'Пользователь {user_name} оплатил заказ на сумму {message.total_amount / 100}₽' \
                   f'\nДанные пользователя: ' \
                   f'\nНомер телефона {message.phone_number}' \
                   f'\nemail {message.email}' \
                   f'\nАдрес заказа {message.shipping_address}' \
                   f'\nСпособ доставки {message.shipping_option_id}'
            await dp.bot.send_message(chat_id=admin, text=text)

        except Exception as err:
            print('иди нахуй!!!')
            logging.exception(err)