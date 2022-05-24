from aiogram import Bot, Dispatcher, executor, types
from keyboard import admin_menu, keyboard_m
from db import add_user, check_existing, check_existing_admin
from validation import check
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from fsms import PasswordFSM, Btn, BtnL
from aiogram.dispatcher import FSMContext
from db import add_admin, add_button
import aiogram.utils.markdown as fmt
from db import get_buttons
import re


API_TOKEN = '5300791081:AAGm4KVZzQhyaLOBA5FN5aZz-CyF-7Hm31Y'

bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
tmp = {}


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    print(message)

    start_menu = types.InlineKeyboardMarkup(row_width=2)
    main_btn = get_buttons()
    start_buttons = []
    for i in main_btn:
        start_buttons.append(types.InlineKeyboardButton(text=i.button_text, url=i.button_link))
    print(start_buttons)
    start_menu.add(*start_buttons)
    exist_user = check_existing(message.chat.id)
    if not exist_user:
        add_user(message.chat.id, message.from_user.first_name, message.from_user.username)
        await message.answer('Hi ' + fmt.hunderline(message.from_user.username) + ' 👀🔥\n' +
                         'This bot contains buttons with links', reply_markup=start_menu)
    else:
        await message.answer('Hi ' + fmt.hunderline(message.from_user.username) + ' 👀🔥\n' +
                         'This bot contains buttons with links', reply_markup=start_menu)


@dp.message_handler(commands=['admin'])
async def start_handler(message: types.Message):
    exist_admin = check_existing_admin(message.chat.id)
    await message.answer('Enter password')
    if not exist_admin:
        await message.answer('Enter password')
    await PasswordFSM.password.set()


@dp.message_handler(state=PasswordFSM)
async def password_validation(message: types.Message, state: FSMContext):
    password = message.text
    valid = check(password)
    if valid:
        add_admin(message.chat.id)
        await message.answer('You have gone to the admin panel', reply_markup=admin_menu)
        await state.finish()
    else:
        await message.answer('Try again')


@dp.callback_query_handler(text='add_button')
async def add_btnnnnn(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer('Enter button name')
    await Btn.text.set()


@dp.message_handler(state=Btn)
async def add_btnnn(message: types.Message, state: FSMContext):
    text = message.text
    tmp[message.chat.id] = {}
    tmp[message.chat.id]['text'] = text
    await state.finish()
    await message.answer('Enter button link')
    await BtnL.link.set()
    print(text)


@dp.message_handler(state=BtnL)
async def add_btnn(message: types.Message, state: FSMContext):
    url_pattern = r'https://[\S]+'
    link = message.text
    print(link)
    urls = re.findall(url_pattern, link)
    print(urls)
    if urls[0]:
        tmp[message.chat.id]['link'] = urls[0]
        print(link)
        await message.answer('Thanks for the data', reply_markup=keyboard_m)
        await state.finish()
    else:
        await message.answer('There is no link here')


@dp.message_handler(Text(equals="Add button ➕"))
async def add_btn(message: types.Message):
    print(tmp)
    add_button(tmp[message.chat.id]['text'], tmp[message.chat.id]['link'])
    await message.answer('Now lets add a button!', reply_markup=types.ReplyKeyboardRemove())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
