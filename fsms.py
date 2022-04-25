from aiogram.dispatcher.filters.state import StatesGroup, State


class PasswordFSM(StatesGroup):
    password = State()


class Btn(StatesGroup):
    text = State()
    link = State()
