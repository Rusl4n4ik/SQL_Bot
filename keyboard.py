from aiogram import types

button_links = {'Очень крутой фонк': 'https://www.youtube.com/watch?v=W9GXqCBAZb0',
                'Рецепт шавухи': 'https://www.youtube.com/watch?v=-rLg9VcEzxw',
                'Что-то дорогое': 'https://www.youtube.com/watch?v=NqjKpE7bdXc',
                'ЕГЭ': 'https://www.youtube.com/watch?v=jxiyffY8-e4'}

start_menu = types.InlineKeyboardMarkup(row_width=2)
start_buttons = [types.InlineKeyboardButton(x, url=button_links[x]) for x in button_links]
start_menu.add(*start_buttons)
admin_menu = types.InlineKeyboardMarkup(row_width=2)
admin_menu.add(types.InlineKeyboardButton('Добавить кнопку', callback_data='add_button'))

