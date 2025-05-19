from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from keyboards import outline_keyboards
from texts import text_messages
from database.add_user import add_user

router = Router()

@router.message(Command('start'))
async def start(message: Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    username = message.from_user.username
    await add_user(user_id, username)

    await message.answer(
        text=text_messages.start,
        reply_markup=outline_keyboards.command_start
    )
