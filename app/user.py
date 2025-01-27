from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from app.database.requests import set_user, get_user, set_start_time, set_end_time, update_user
from datetime import datetime
import app.keyboards as kb

user_router = Router()

class Reg(StatesGroup):
    contact = State()

class Time(StatesGroup):
    start_time = State()
    end_time = State()
    current_time = State()

class MainMenu(StatesGroup):
    menu = State()

def time_now():
    return datetime.now().strftime('%H:%M')

def date_now():
    return datetime.now().strftime('%d.%m.%Y')

@user_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    user = await set_user(message.from_user.id, message.from_user.username)

    if user:
        # await state.set_state(MainMenu.menu)
        await message.answer(f"Приветсвтвую {message.from_user.username}. Выбери действие из списка ниже!", reply_markup=kb.main)
    else:
        await state.set_state(Reg.contact)
        await message.answer("Приветсвтвую, пройдите регистрацию.\nВведите ваш контакт", reply_markup=kb.contact)


@user_router.message(Reg.contact, F.contact)
async def reg_contact(message: Message, state: FSMContext):
    # data = await state.get_data()
    await update_user(message.from_user.id, message.contact.phone_number)
    await state.set_state(MainMenu.menu)
    await message.answer('Вы успешно авторизовались теперь вы в главном меню.\nВыберите действие', reply_markup=kb.main)
    

@user_router.message(MainMenu.menu)
async def main_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Главное меню", reply_markup=kb.main)


@user_router.message(F.text == 'Начало сессии')
async def get_service(message: Message, state: FSMContext):
    await state.set_state(Time.start_time)
    await message.answer('Выберите время начала', reply_markup=kb.time_kb)


@user_router.message(Time.start_time, F.text == 'Текущее время')
async def current_time(message: Message, state: FSMContext):
    await set_start_time(message.from_user.id, date_now(), time_now())
    await state.set_state(MainMenu.menu)
    await message.answer(f'Время начала успешно записано\n{date_now()}\n{time_now()}'
                         , reply_markup=kb.back2menu)


@user_router.message(F.text == 'Конец сессии')
async def get_service(message: Message, state: FSMContext):
    await state.set_state(Time.end_time)
    await message.answer('Выберите время окончания', reply_markup=kb.time_kb)


@user_router.message(Time.end_time, F.text == 'Текущее время')
async def current_time(message: Message, state: FSMContext):
    await set_end_time(message.from_user.id, date_now(), time_now())
    await state.set_state(MainMenu.menu)
    await message.answer(f'Время окончания успешно записано\n{date_now()}\n{time_now()}'
                         ,reply_markup=kb.back2menu)
