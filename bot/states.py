from aiogram.fsm.state import StatesGroup, State


class Register(StatesGroup):
    name = State()
    gender = State()
    age = State()
    height = State()
    weight = State()
