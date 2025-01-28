from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
from app.states import Reg, Time, MainMenu, Analysis
from app.database.requests import set_user, get_status, set_start_time, set_end_time, update_user, get_work_hours
from app.logic import is_valid_time_format, datetime_from_message, time_now

user_router = Router()

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

#---------------------------------TimeStart---------------------------------#
@user_router.message(F.text == 'Начало сессии')
async def get_service(message: Message, state: FSMContext):
    await state.set_state(Time.start_time)
    await message.answer('Выберите время начала', reply_markup=kb.time_kb)


@user_router.message(Time.start_time, F.text == 'Текущее время')
async def current_time(message: Message, state: FSMContext):
    record = await get_status(message.from_user.id)
    if record == True:
         await state.set_state(Time.end_time)
         await message.answer('У вас есть не оконченая сессия.\nЗапишите время конца сессии', reply_markup=kb.time_kb)
    else:
        await set_start_time(message.from_user.id, time_now())
        await state.set_state(MainMenu.menu)
        await message.answer(f'Время начала успешно записано\n{time_now()}', reply_markup=kb.back2menu)


@user_router.message(Time.start_time, F.text == 'Записать время вручную')
async def manual_start(message: Message, state: FSMContext):
    record = await get_status(message.from_user.id)
    if record == True:
         await state.set_state(Time.end_time)
         await message.answer('У вас есть не оконченая сессия.\nЗапишите время конца сессии', reply_markup=kb.time_kb)
    else:
        await state.set_state(Time.enter_manual_start_time)
        await message.answer('Введите время начала в формате\nПример: 28.01.2025 13:15')

@user_router.message(Time.enter_manual_start_time)
async def enter_manual_start_time(message: Message, state: FSMContext):
    if is_valid_time_format(message.text):
        await set_start_time(message.from_user.id, datetime_from_message(message))
        await state.set_state(MainMenu.menu)
        await message.answer(f'Время начала успешно записано\n{datetime_from_message(message)}',reply_markup=kb.back2menu)
    else:
        await message.answer('Неверный формат времени, попробуйте еще раз')

#---------------------------------TimeEnd---------------------------------#
@user_router.message(F.text == 'Конец сессии')
async def get_service(message: Message, state: FSMContext):
    await state.set_state(Time.end_time)
    await message.answer('Выберите время окончания', reply_markup=kb.time_kb)


@user_router.message(Time.end_time, F.text == 'Текущее время')
async def current_time(message: Message, state: FSMContext):
    record = await get_status(message.from_user.id)
    if record == False:
        await state.set_state(Time.start_time)
        await message.answer('Время окончания не записано.\nЗапишите время начала сессии', reply_markup=kb.time_kb)
    else:
        await set_end_time(message.from_user.id, time_now())
        await state.set_state(MainMenu.menu)
        await message.answer(f'Время окончания успешно записано\n{time_now()}', reply_markup=kb.back2menu)
    
@user_router.message(Time.end_time, F.text == 'Записать время вручную')
async def manual_end(message: Message, state: FSMContext):
    record = await get_status(message.from_user.id)
    if record == False:
         await state.set_state(Time.start_time)
         await message.answer('У вас есть не начатая сессия.\nЗапишите время начала сессии', reply_markup=kb.time_kb)
    else:
        await state.set_state(Time.enter_manual_end_time)
        await message.answer('Введите время окончания в формате\nПример: 28.01.2025 13:15')

@user_router.message(Time.enter_manual_end_time)
async def enter_manual_end_time(message: Message, state: FSMContext):
    if is_valid_time_format(message.text):
        await set_end_time(message.from_user.id, datetime_from_message(message))
        await state.set_state(MainMenu.menu)
        await message.answer(f'Время окончания успешно записано\n{datetime_from_message(message)}',reply_markup=kb.back2menu)
    else:
        await message.answer('Неверный формат времени, попробуйте еще раз')

#---------------------------------Analys---------------------------------#
@user_router.message(F.text == 'Аналитика')
async def analysis(message: Message, state: FSMContext):
    await state.set_state(MainMenu.menu)
    await message.answer('Аналитика', reply_markup=kb.analysis)

@user_router.message(F.text == 'Сводка за день')
async def summary_day(message: Message):
    total_hours = await get_work_hours(message.from_user.id, 'day')
    await message.answer(f'Вы отработали {total_hours:.2f} часов за день.')

@user_router.message(F.text == 'Сводка за неделю')
async def summary_week(message: Message):
    total_hours = await get_work_hours(message.from_user.id, 'week')
    await message.answer(f'Вы отработали {total_hours:.2f} часов за неделю.')

@user_router.message(F.text == 'Сводка за месяц')
async def summary_month(message: Message):
    total_hours = await get_work_hours(message.from_user.id, 'month')
    await message.answer(f'Вы отработали {total_hours:.2f} часов за месяц.')
