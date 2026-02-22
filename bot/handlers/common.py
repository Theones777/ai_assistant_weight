from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.handlers.steps import STEPS

common_router = Router()

@common_router.message(StateFilter(None), Command(commands=["start"]))
async def message_start_handler(message: Message, state: FSMContext, bot: Bot):
    first_state = next(iter(STEPS))
    await state.set_state(first_state)
    await message.answer(STEPS[first_state]["question"])


@common_router.message(StateFilter(*STEPS.keys()))
async def register_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()

    # Находим объект State
    state_obj = next(s for s in STEPS if s.state == current_state)
    step_config = STEPS[state_obj]

    # Валидация
    if not step_config["validator"](message.text):
        await message.answer(step_config["error"])
        return

    # Сохраняем данные
    await state.update_data(**{
        step_config["field"]: message.text
    })

    # Определяем следующий шаг
    states_list = list(STEPS.keys())
    current_index = states_list.index(state_obj)

    # Если последний шаг — завершаем
    if current_index == len(states_list) - 1:
        data = await state.get_data()

        print("Данные пользователя:")
        print(data)

        await message.answer("Спасибо. Данные сохранены.")
        await state.clear()
        return

    # Иначе переходим дальше
    next_state = states_list[current_index + 1]
    await state.set_state(next_state)
    await message.answer(STEPS[next_state]["question"])


@common_router.message(StateFilter(None))
async def dialog_handler(message: Message, bot: Bot):
    ai_agent = bot.ai
    response = await ai_agent.make_request(message.text)
    await message.answer(response)
