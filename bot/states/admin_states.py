from aiogram.fsm.state import State, StatesGroup

class AdminMainSG(StatesGroup):
    verifying = State()
    mailing = State()
    phone = State()
    api_id = State()
    api_hash = State()
    app_version = State()
    device_model = State()
    system_version = State()
    lang_code = State()
    password = State()
    proxy_scheme = State()
    proxy_host = State()
    proxy_port = State()
    proxy_username = State()
    proxy_password = State()
    enter_code = State()