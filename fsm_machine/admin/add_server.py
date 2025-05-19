from aiogram.fsm.state import State, StatesGroup

class ServerData(StatesGroup):
    api_url = State()
    ip = State()
    password = State()
    location_country= State()
    location_city = State()