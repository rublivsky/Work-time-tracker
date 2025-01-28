import pytz
from datetime import datetime
from aiogram.types import Message

def local_time(time_str: str, timezone_str: str):
    try:
        # Пробуем преобразовать введенную строку в дату и время
        input_time = datetime.strptime(time_str, '%d.%m.%Y %H:%M')
        # Устанавливаем часовой пояс для введенного времени
        input_time = input_time.replace(tzinfo=pytz.timezone(timezone_str))
        # Текущее время в UTC
        utc_time = datetime.utcnow().replace(tzinfo=pytz.utc)
        # Перевод времени в нужный часовой пояс
        local_time = utc_time.astimezone(input_time.tzinfo)
        return local_time.strftime('%d.%m.%Y %H:%M')
    except (ValueError, pytz.UnknownTimeZoneError):
        return None

def time_now():
    tz = pytz.timezone('Europe/Kiev')  # Заменить на свой нужный часовой пояс
    return datetime.now(tz).strftime('%d.%m.%Y %H:%M')


def is_valid_time_format(time_str: str):
    try:
        # Пробуем преобразовать введенную строку в дату и время
        datetime.strptime(time_str, '%d.%m.%Y %H:%M')
        return True
    except ValueError:
        return False

def datetime_from_message(message: Message):
    return datetime.strptime(message.text, '%d.%m.%Y %H:%M').strftime('%d.%m.%Y %H:%M')

