from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from texts import text_messages
from keyboards import inline_keyboards

router = Router()

@router.message(Command('admin'))
async def admin_panel(message: Message):
    await message.answer(
        text=text_messages.admin_panel,
        reply_markup=inline_keyboards.admin_panel()
    )