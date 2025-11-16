from aiogram.fsm.state import State, StatesGroup

class AdminMainSG(StatesGroup):
    menu = State()
    contacts = State()
    database = State()
    mailing_text = State()
    mailing_photo = State()
    clean_contacts = State()
    sure_to_mail = State()