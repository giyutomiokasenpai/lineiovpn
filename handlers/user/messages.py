from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from texts import text_keyboards, text_messages
from keyboards import inline_keyboards
from database.get_user_keys import get_user_key_names
from database.change_settings import change_name
from fsm_machine.fsm_classes import ChangeName

router = Router()

@router.message(F.text == text_keyboards.my_keys)
async def my_keys(message: Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    if await get_user_key_names(user_id) != []:
        await message.answer(
            text=text_messages.get_my_keys,
            reply_markup=await inline_keyboards.get_keys(user_id)
        )
    else:
        await message.answer(
            text=text_messages.no_keys,
            reply_markup=inline_keyboards.add_key()
        )

@router.message(F.text == text_keyboards.buy_key)
async def buy_key(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text=text_messages.buy_key,
        reply_markup=inline_keyboards.buy_key()
    )

@router.message(ChangeName.name)
async def set_new_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    key_id = data.get('key_id')
    name = data.get('name')
    new_name = await change_name(key_id, name)
    await state.clear()

    await message.answer(
        text=f'Имя было изменено на {new_name}'
    )