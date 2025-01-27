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
        # keyboard.add(InlineKeyboardButton(text=barber.name, callback_data=f'barber_{barber.id}'))
        [KeyboardButton(text='Текущее время')],
        [KeyboardButton(text='Записать время вручную')],
    ], resize_keyboard=True)
