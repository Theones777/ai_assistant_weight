from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

common_router = Router()


@common_router.message(StateFilter(None), Command(commands=["start"]))
async def message_start_handler(msg: Message, state: FSMContext, bot: Bot):
    db_client = bot.db
    print(db_client)
    await state.clear()
    await msg.answer("db_client", reply_markup=ReplyKeyboardRemove())
