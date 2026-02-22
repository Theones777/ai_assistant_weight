from collections import OrderedDict

from bot.states import Register


async def normalize_gender(input_text: str):
    if "м" in input_text.lower():
        return "мужчина"
    return "женщина"


STEPS = OrderedDict({
    Register.name: {
        "field": "name",
        "question": "Введите ваше имя:",
        "validator": lambda x: True,
        "error": ""
    },
    Register.gender: {
        "field": "gender",
        "question": "Введите Ваш пол:",
        "validator": lambda x: True,
        "normalizer": normalize_gender,
        "error": ""
    },
    # Register.age: {
    #     "field": "age",
    #     "question": "Введите возраст:",
    #     "validator": lambda x: x.isdigit(),
    #     "error": "Возраст должен быть числом."
    # },
    # Register.height: {
    #     "field": "height",
    #     "question": "Введите Ваш рост:",
    #     "validator": lambda x: x.isdigit(),
    #     "error": "Рост должен быть числом."
    # },
    # Register.weight: {
    #     "field": "weight",
    #     "question": "Введите Ваш вес:",
    #     "validator": lambda x: x.isdigit(),
    #     "error": "Вес должен быть числом."
    # },
})
