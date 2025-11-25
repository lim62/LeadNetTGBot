from aiogram.fsm.state import State, StatesGroup

class UserMainSG(StatesGroup):
    fastlane = State()
    product = State()
    sources_traffic = State()
    model = State()
    economics = State()
    time = State()
    load_chats = State()
    load_offer = State()