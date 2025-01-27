import sqlite3
from datetime import datetime
from aiogram import Router, types
from aiogram.filters import Command
import app.keyboards as kb

router = Router()
cur_date = datetime.now().strftime('%Y-%m-%d')
#'%m-%d %H:%M'
def is_valid_time_format(time_str: str):
    try:
        # Пробуем преобразовать введенную строку в дату и время
        datetime.strptime(time_str, '%m-%d %H:%M')
        return True
    except ValueError:
        return False

def get_db_connection():
    conn = sqlite3.connect('database/db.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn

def is_authorized(telegram_id: int):
    auth = get_db_connection().cursor()
    auth.execute("SELECT is_authorized FROM users WHERE telegram_id = ?", (telegram_id,))
    result = auth.fetchone()
    return result[0] if result else False

def username(message: types.Message):
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name or ""  # Если фамилия отсутствует, используем пустую строку
    full_name = f"{first_name} {last_name}".strip()  # Убираем лишние пробелы
    return full_name

# Хендлер /start - авторизация
@router.message(Command("start"))
async def start(message: types.Message):
    conn = get_db_connection()
    cursor = conn.cursor()
    telegram_id = message.from_user.id
    full_name = username(message)

    if is_authorized(message.from_user.id):
        await message.answer("Успешная авторизация.")
        # Обновляем статус авторизации
        cursor.execute("UPDATE users SET is_authorized = ?, username = ? WHERE telegram_id = ?", (1, full_name, telegram_id))
        conn.commit()
    else:
        await message.reply("Успешная авторизация.")
        cursor.execute("INSERT INTO users (telegram_id, username, is_authorized) VALUES (?, ?, ?)", (telegram_id, full_name, 1))
        conn.commit()
    conn.close()
    await message.answer("Выберите действие:", reply_markup=kb.main())

# Хендлер для начала рабочей сессии
@router.message(Command("start_session"))
@router.message(lambda message: message.text.lower() == "начало сессии")
async def start_session(message: types.Message):
    telegram_id = int(message.from_user.id)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM work_time WHERE telegram_id = ?", (telegram_id,))
    session = cursor.fetchone()
    
    if session == 1:
        await message.answer("У вас уже есть активная рабочая сессия.")
        # Добавить кнопки для завершения сессии с помощью сообщения
    else:
        # Создание новой рабочей сессии
        start_time = datetime.now().strftime('%m-%d %H:%M:%S')
        cursor.execute("INSERT INTO work_time (telegram_id, date, start_time, status) VALUES (?, ?, ?, ?)",
                       (telegram_id, cur_date, start_time, 1))
        conn.commit()
        await message.answer(f"Сессия начата в {start_time}.")
    conn.close()
    await message.answer("Выберите действие:", reply_markup=kb.main())

# Хендлер для завершения рабочей сессии
@router.message(Command("end_session"))
@router.message(lambda message: message.text.lower() == "конец сессии")
async def end_session(message: types.Message):
    telegram_id = int(message.from_user.id)
    conn = get_db_connection()
    cursor = conn.cursor()
    end_time = datetime.now().strftime('%m-%d %H:%M:%S')

    # Проверяем наличие активной сессии
    cur_date = datetime.now().strftime('%Y-%m-%d')
    cursor.execute("SELECT id, status FROM work_time WHERE telegram_id = ? AND date = ? ORDER BY start_time DESC", 
                   (telegram_id, cur_date))
    session = cursor.fetchone()

    if not session or session[1] == 0:
        await message.answer("У вас нет активной сессии. Пожалуйста, введите время начала сессии в формате ММ-ДД ЧЧ:ММ")

        @router.message()
        async def handle_start_time_input(new_message: types.Message):
            start_time = new_message.text.strip()
            if is_valid_time_format(start_time):
                # Вставляем новое начало сессии в базу данных
                cursor.execute("INSERT INTO work_time (telegram_id, status, start_time, date, end_time) VALUES (?, ?, ?, ?, ?)",
                               (telegram_id, 0, start_time, cur_date, end_time))
                conn.commit()
                await new_message.answer(f"Запись добавлена. Сессия начата с времени: {start_time}\n Оконачена в {end_time}.")
            else:
                await new_message.answer("Неверный формат времени. Попробуйте снова.\n(формат: ММ-ДД ЧЧ:ММ)")

    else:
        # Если сессия активна, завершаем её
        cursor.execute("UPDATE work_time SET end_time = ?, status = ? WHERE id = ?", 
                       (end_time, 0, session[0]))
        # conn.commit()
        await message.answer(f"Сессия завершена. Время окончания: {end_time}.")
    conn.commit()
    # conn.close()
    # await message.answer("Выберите действие:", reply_markup=main_menu())

# Хендлер для просмотра аналитикич
@router.message(Command("analysis"))
@router.message(lambda message: message.text.lower() == "аналитика")
async def analysis(message: types.Message):
    telegram_id = message.from_user.id
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Период (за текущий день для примера)
    start_date = datetime.now().strftime('%m-%d') + ' 00:00:00'
    end_date = datetime.now().strftime('%m-%d') + ' 23:59:59'
    
    cursor.execute("SELECT * FROM work_time WHERE telegram_id = ? AND start_time BETWEEN ? AND ?",
                   (telegram_id, start_date, end_date))
    sessions = cursor.fetchall()
    
    total_hours = len(sessions)  # Простой подсчет для примера
    await message.answer(f"Общее количество сессий за сегодня: {total_hours}")
    
    conn.close()