from aiogram.fsm.state import State, StatesGroup

class UserMainSG(StatesGroup):
    name = State()
    age = State()
    story = State()
    design = State()
    final = State()