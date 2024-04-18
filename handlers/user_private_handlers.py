from aiogram import types, Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_add_topic, orm_get_topic
from kbds import reply

user_private_router = Router()


class AddDataState(StatesGroup):
    data_name = State()


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Привет, данный бот предназначен для хранения тем на открытый микрофон",
                         reply_markup=reply.start_keyboard)


@user_private_router.message(StateFilter(None), F.text.lower() == 'добавить тему')
async def add_data(message: types.Message, state: FSMContext):
    await message.answer("Введите тему:", reply_markup=reply.remove_kbd)
    await state.set_state(AddDataState.data_name)


@user_private_router.message(AddDataState.data_name, F.text)
async def process_topic(message: types.Message, state: FSMContext, session: AsyncSession):
    chat_id = message.chat.id
    text = message.text
    await state.update_data(data_name=text)
    data = await state.get_data()
    try:
        await orm_add_topic(session, data, chat_id)
        await message.answer("Спасибо! Ваша информация сохранена.")
        await state.clear()
        await message.answer("Хотите добавить ещё тему?", reply_markup=reply.close_keyboard)
    except Exception as e:
        await message.answer("Ошибка, не получилось добавить тему!")
        print("вот ошибка: ")
        print(e)
        await state.clear()


@user_private_router.message(F.text.lower().contains('да'))
async def text_yes(message: types.Message, state: FSMContext):
    await add_data(message, state)


@user_private_router.message(F.text.lower().contains('нет'))
async def text_no(message: types.Message):
    await message.answer("Пока!", reply_markup=reply.remove_kbd)
    await message.leave_chat(message.chat.id)


@user_private_router.message(F.text.lower() == "посмотреть список тем")
async def show_data_cmd(message: types.Message, session: AsyncSession):
    for data in await orm_get_topic(session):
        await message.answer(data.open_mic_topic)
