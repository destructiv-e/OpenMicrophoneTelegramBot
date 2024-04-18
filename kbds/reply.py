from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить тему")
        ],
        {
            KeyboardButton(text="Посмотреть список тем")
        }
    ],
    resize_keyboard=True,
    input_field_placeholder="Что вы хотите сделать?"
)

close_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Да")
        ],
        {
            KeyboardButton(text="Нет")
        }
    ],
    resize_keyboard=True,
    input_field_placeholder="Что вы хотите сделать?"
)

remove_kbd = ReplyKeyboardRemove()
