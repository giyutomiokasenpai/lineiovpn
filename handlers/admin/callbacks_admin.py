from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from texts import text_messages
from fsm_machine.admin.add_server import ServerData

router = Router()

@router.callback_query(F.data == 'add_server')
async def add_server(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text=text_messages.insert_api_url
    )
    await state.set_state(ServerData.api_url)
    await callback.answer()