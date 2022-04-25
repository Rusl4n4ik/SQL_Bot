from aiogram import Bot, Dispatcher, executor, types
from keyboard import start_menu, admin_menu
from db import add_user, check_existing, add_admin, check_existing_admin
from validation import check
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from fsms import PasswordFSM, Btn
from aiogram.dispatcher import FSMContext
from db import add_admin

API_TOKEN = '5300791081:AAGm4KVZzQhyaLOBA5FN5aZz-CyF-7Hm31Y'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    print(message)
    add_user(message.chat.id, message.from_user.first_name, message.from_user.username)
    await message.answer('Вы нажали на старт', reply_markup=start_menu)


@dp.message_handler(commands=['admin'])
async def start_handler(message: types.Message):
    exist_admin = check_existing_admin(message.chat.id)
    if not exist_admin:
        await message.answer('Введите пароль')
    else:
        await message.answer('Вы перешли в админ панель', reply_markup=admin_menu)
    await PasswordFSM.password.set()


@dp.message_handler(state=PasswordFSM)
async def password_validation(message: types.Message, state: FSMContext):
    password = message.text
    valid = check(password)
    if valid:
        add_admin(message.chat.id)
        await message.answer('Вы перешли в админ панель', reply_markup=admin_menu)
        await state.finish()
    else:
        await message.answer('Попробуйте еще раз')


@dp.callback_query_handler(text='add_button')
async def add_button(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer('Введите название кнопки')
    await Btn.text.set()


@dp.message_handler(state=Btn)
async def add_button(message: types.Message, state=FSMContext):
    text = message.text
    print(text)
    await Btn.next()
    await message.answer('Теперь введите ссылку')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
