import pytz
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from app.database.requests import set_user, get_status, set_start_time, set_end_time, update_user
from datetime import datetime
import app.keyboards as kb

user_router = Router()

class Reg(StatesGroup):
    contact = State()

class Time(StatesGroup):
    start_time = State()
    end_time = State()
    current_time = State()
    enter_manual_end_time = State()
    enter_manual_start_time = State()

class MainMenu(StatesGroup):
    menu = State()

def local_time(time_str: str, timezone_str: str):
    try:
        # Пробуем преобразовать введенную строку в дату и время
        input_time = datetime.strptime(time_str, '%m-%d %H:%M')
        # Устанавливаем часовой пояс для введенного времени
        input_time = input_time.replace(tzinfo=pytz.timezone(timezone_str))
        # Текущее время в UTC
        utc_time = datetime.utcnow().replace(tzinfo=pytz.utc)
        # Перевод времени в нужный часовой пояс
        local_time = utc_time.astimezone(input_time.tzinfo)
        return local_time.strftime('%d.%m %H:%M')
    except (ValueError, pytz.UnknownTimeZoneError):
        return None

def time_now():
    tz = pytz.timezone('Europe/Kiev')  # Заменить на свой нужный часовой пояс
    return datetime.now(tz).strftime('%H:%M')

def date_now():
    return datetime.now().strftime('%d.%m')

def is_valid_time_format(time_str: str):
    try:
        # Пробуем преобразовать введенную строку в дату и время
        datetime.strptime(time_str, '%m-%d %H:%M')
        return True
    except ValueError:
        return False

def date_from_message(message: Message):
    return datetime.strptime(message.text, '%m-%d %H:%M').strftime('%d.%m')

def time_from_message(message: Message):
    return datetime.strptime(message.text, '%m-%d %H:%M').strftime('%H:%M')

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
    await message.answer('Вы успешно авторизовались!\nВыберите действие', reply_markup=kb.main)
    

@user_router.message(MainMenu.menu, F.text == 'В главное меню')
async def main_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Главное меню", reply_markup=kb.main)


@user_router.message(F.text == 'Начало сессии')
async def get_service(message: Message, state: FSMContext):
    await state.set_state(Time.start_time)
    await message.answer('Выберите время начала', reply_markup=kb.time_kb)


@user_router.message(Time.start_time, F.text == 'Текущее время')
async def current_time(message: Message, state: FSMContext):
    record = await get_status(message.from_user.id)
    if record == True:
         await state.set_state(Time.end_time)
         await message.answer('У вас есть не оконченая сессия.\nЗапишите время конца сессии', 
                              reply_markup=kb.end_time_kb)
    else:
        await set_start_time(message.from_user.id, date_now(), time_now())
        await state.set_state(MainMenu.menu)
        await message.answer(f'Время начала успешно записано\n{date_now()}\n{time_now()}'
                            , reply_markup=kb.back2menu)


@user_router.message(Time.start_time, F.text == 'Записать время вручную')
async def manual_start(message: Message, state: FSMContext):
    record = await get_status(message.from_user.id)
    if record == True:
         await state.set_state(Time.end_time)
         await message.answer('У вас есть не оконченая сессия.\nЗапишите время конца сессии', 
                              reply_markup=kb.end_time_kb)
    else:
        await state.set_state(Time.enter_manual_start_time)
        await message.answer('Введите время начала в формате\nмм-дд чч:мм')

@user_router.message(Time.enter_manual_start_time)
async def enter_manual_start_time(message: Message, state: FSMContext):
    if is_valid_time_format(message.text):
        await set_start_time(message.from_user.id, date_from_message(message), time_from_message(message))
        await state.set_state(MainMenu.menu)
        await message.answer(f'Время начала успешно записано\n{date_from_message(message)}\n{time_from_message(message)}'
                             ,reply_markup=kb.back2menu)
    else:
        await message.answer('Неверный формат времени, попробуйте еще раз')


@user_router.message(F.text == 'Конец сессии')
async def get_service(message: Message, state: FSMContext):
    await state.set_state(Time.end_time)
    await message.answer('Выберите время окончания', reply_markup=kb.time_kb)


@user_router.message(Time.end_time, F.text == 'Текущее время')
async def current_time(message: Message, state: FSMContext):
    record = await get_status(message.from_user.id)
    if record == False:
        await state.set_state(Time.start_time)
        await message.answer('Время окончания не записано.\nЗапишите время начала сессии', 
                             reply_markup=kb.time_kb)
    else:
        await set_end_time(message.from_user.id, date_now(), time_now())
        await state.set_state(MainMenu.menu)
        await message.answer(f'Время окончания успешно записано\n{date_now()}\n{time_now()}'
                         ,reply_markup=kb.back2menu)
    
@user_router.message(Time.end_time, F.text == 'Записать время вручную')
async def manual_end(message: Message, state: FSMContext):
    record = await get_status(message.from_user.id)
    if record == False:
         await state.set_state(Time.start_time)
         await message.answer('У вас есть не начатая сессия.\nЗапишите время начала сессии', 
                              reply_markup=kb.time_kb)
    else:
        await state.set_state(Time.enter_manual_end_time)
        await message.answer('Введите время окончания в формате\nмм-дд чч:мм')

@user_router.message(Time.enter_manual_end_time)
async def enter_manual_end_time(message: Message, state: FSMContext):
    if is_valid_time_format(message.text):
        await set_end_time(message.from_user.id, date_from_message(message), time_from_message(message))
        await state.set_state(MainMenu.menu)
        await message.answer(f'Время окончания успешно записано\n{date_from_message(message)}\n{time_from_message(message)}'
                             ,reply_markup=kb.back2menu)
    else:
        await message.answer('Неверный формат времени, попробуйте еще раз')
