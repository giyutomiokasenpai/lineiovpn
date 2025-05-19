from aiogram.fsm.state import State, StatesGroup

class ChangeName(StatesGroup):
    key_id = State()
    name = State()

class SubscriptionContinue(StatesGroup):
    key_id = State()
    duration = State()