from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from database.get_user_keys import get_vpn_keys
from database.insert_new_key import insert_new_key
from database.change_settings import subscription_continue_db, change_location_db, recreate_key_db
from database.get_user_keys import get_user_key_names
from texts import text_messages
from fsm_machine.fsm_classes import ChangeName, SubscriptionContinue
from keyboards import inline_keyboards

router = Router()

@router.callback_query(F.data == 'close')
async def close(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.answer()

@router.callback_query(F.data == 'add_key')
async def add_key(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        text=text_messages.buy_key,
        reply_markup=inline_keyboards.buy_key()
    )

@router.callback_query(lambda c: c.data.startswith('key_id_'))
async def get_vpn_key(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    key_id = callback.data[7:]
    data = list(await get_vpn_keys(key_id))[0]
    name = data[1]
    accessUrl = f'{data[0]}#{name}'
    duration = data[2]
    end_at = data[3]
    location_country = data[4]
    location_city = data[5]

    text = (f'Название: {name}\n\nТариф: {duration} месяц\n\nДействует до: {end_at}\n\nЛокация: {location_city}, {location_country}\n\nКлюч: \n`{accessUrl}`')

    await callback.message.edit_text(
        text=text,
        reply_markup=inline_keyboards.key_setting(key_id, location_city),
        parse_mode='MarkDown'
    )
    await callback.answer()

@router.callback_query(lambda c: c.data.startswith('buy_key_'))
async def buy_key(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    username = callback.from_user.username
    user_id = callback.from_user.id
    duration = callback.data[-1] if callback.data[-2] == '_' else callback.data[-2:]
    await insert_new_key(username, duration, user_id)
    
    await callback.message.edit_text(
        text=text_messages.buy_key_done
    )
    await callback.answer()

@router.callback_query(lambda c: c.data.startswith('change_name_'))
async def change_name(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text=text_messages.change_name,
        reply_markup=inline_keyboards.stop_change_name()
    )
    await state.set_state(ChangeName.key_id)
    await state.update_data(key_id=callback.data[12:])
    await state.set_state(ChangeName.name)
    await callback.answer()

@router.callback_query(lambda c: c.data.startswith('change_location_'))
async def change_location(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    data = callback.data.split('_')
    key_id = data[-1]
    current_location_city = data[-2]
    await callback.message.edit_text(
        text=text_messages.change_location,
        reply_markup=await inline_keyboards.change_location(key_id, current_location_city)
    )
    await callback.answer()

@router.callback_query(lambda c: c.data.startswith('recreate_key_'))
async def recreate_key(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    key_id = callback.data[13:]
    await recreate_key_db(key_id)

    data = list(await get_vpn_keys(key_id))[0]
    name = data[1]
    accessUrl = f'{data[0]}#{name}'
    duration = data[2]
    end_at = data[3]
    location_country = data[4]
    location_city = data[5]

    text = (f'Название: {name}\n\nТариф: {duration} месяц\n\nДействует до: {end_at}\n\nЛокация: {location_city}, {location_country}\n\nКлюч: \n`{accessUrl}`')

    await callback.message.delete()
    await callback.message.answer(
        text=text,
        reply_markup=inline_keyboards.key_setting(key_id, location_city),
        parse_mode='MarkDown'
    )
    await callback.answer(
        text=text_messages.recreate_key_done
    )

@router.callback_query(lambda c: c.data.startswith('set_location_'))
async def set_location(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    data = callback.data.split('_')
    key_id = data[-1]
    location_city = data[-2]
    location_country = await change_location_db(key_id, location_city)
    await callback.message.edit_text(
        text=f'{text_messages.change_location_done} {location_city}, {location_country}'
    )

@router.callback_query(lambda c: c.data.startswith('subscription_continue_'))
async def subscription_continue(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    key_id = callback.data[22:]
    name = list(await get_vpn_keys(key_id=key_id))[0][1]

    await callback.message.edit_text(
        text=f'{text_messages.subscription_continiue} {name}',
        reply_markup=inline_keyboards.subscription_continue(key_id)
    )
    await callback.answer()

@router.callback_query(lambda c: c.data.startswith('continue_'))
async def buy_key_continue(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    key_id = callback.data[11:]
    duration = callback.data[9]
    await subscription_continue_db(key_id, duration)

    await callback.answer(
        text=f'{text_messages.subscription_continiue_done_one} {duration} {text_messages.subscription_continiue_done_two}'
    )

@router.callback_query(F.data == 'go_back_from_key_settings')
async def go_back_from_key_settings(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    user_id = callback.from_user.id
    if await get_user_key_names(user_id) != []:
        await callback.message.edit_text(
            text=text_messages.get_my_keys,
            reply_markup=await inline_keyboards.get_keys(user_id)
        )
    else:
        await callback.message.edit_text(
            text=text_messages.no_keys,
            reply_markup=inline_keyboards.add_key()
        )
    await callback.answer()