from aiogram.fsm.state import StatesGroup, State


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
    
class Analysis(StatesGroup):
    analysis = State()
    analysis_day = State()
    analysis_week = State()
    analysis_month = State()
    analysis_menu_test = State()
    
