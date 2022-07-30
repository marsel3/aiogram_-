from loader import dp
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram import types
from states import test


@dp.message_handler(Command('register'))
async def register(message: types.Message):
    await message.answer('HELLO!')
    await test.test1.set()


@dp.message_handler(state=test.test1)
async def state1(message: types.Message, state: FSMContext):

    answer = message.text
    if answer == 'HELLO':
        await message.answer('a-a-a-a')
    else:
        await state.update_data(test1=answer)

        data = await state.get_data()
        await message.answer(f'Привет, {data.get("test2")},  я тебя запомнил!')
        await state.finish()