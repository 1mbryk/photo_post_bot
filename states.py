from aiogram.fsm.state import State, StatesGroup


class States(StatesGroup):
    default_state = State()
    waiting_path = State()
