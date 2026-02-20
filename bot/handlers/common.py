from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

common_router = Router()


@common_router.message(StateFilter(None), Command(commands=["start"]))
async def message_start_handler(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer("message", reply_markup=ReplyKeyboardRemove())
