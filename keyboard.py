from aiogram import types
from db import get_buttons

admin_menu = types.InlineKeyboardMarkup(row_width=2)
admin_menu.add(types.InlineKeyboardButton('Add new button', callback_data='add_button'))
keyboard_m = types.ReplyKeyboardMarkup(resize_keyboard=True)
new_btns = types.InlineKeyboardMarkup(row_width=2)
button = ['Add button ➕']
keyboard_m.add(*button)

