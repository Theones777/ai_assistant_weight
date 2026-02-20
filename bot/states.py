from aiogram.fsm.state import StatesGroup, State


class Welcome(StatesGroup):
    gender = State()
    age = State()
    height = State()
    weight = State()
