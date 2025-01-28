from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Начало сессии"), KeyboardButton(text="Конец сессии")],
        [KeyboardButton(text="Аналитика")]
], resize_keyboard=True)

back2menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="В главное меню")]
], resize_keyboard=True)

contact = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Отправить контакт', request_contact=True)]
], resize_keyboard=True, input_field_placeholder='Нажмите кнопку ниже.')

time_kb = ReplyKeyboardMarkup(keyboard = [
        [KeyboardButton(text='Текущее время')],
        [KeyboardButton(text='Записать время вручную')]
        # ,[KeyboardButton(text="В главное меню")]
    ], resize_keyboard=True)

analysis = ReplyKeyboardMarkup(keyboard = [
    [KeyboardButton(text='Сводка за месяц'), KeyboardButton(text='Сводка за неделю')],
    [KeyboardButton(text='Сводка за день')],
    [KeyboardButton(text="В главное меню")]
], rezie_keyboard=True)