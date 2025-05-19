from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.get_user_keys import get_user_key_names, get_servers
from texts import text_keyboards


async def get_keys(user_id):
    keys = await get_user_key_names(user_id)

    builder = InlineKeyboardBuilder()
    for key in keys:
        builder.add(
            InlineKeyboardButton(text=key[1], callback_data=f'key_id_{key[0]}')
        )
    builder.add(
        InlineKeyboardButton(text=text_keyboards.close, callback_data=f'close')
    )
    builder.adjust(1)
    keyboard = builder.as_markup()
    return keyboard

def buy_key():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text_keyboards.buy_key_1_month, callback_data='buy_key_1')],
            [InlineKeyboardButton(text=text_keyboards.buy_key_3_months, callback_data='buy_key_3')],
            [InlineKeyboardButton(text=text_keyboards.buy_key_6_months, callback_data='buy_key_6')],
            [InlineKeyboardButton(text=text_keyboards.buy_key_12_months, callback_data='buy_key_12')],
            [InlineKeyboardButton(text=text_keyboards.close, callback_data='close')]
        ]
    )
    return keyboard

def key_setting(key_id, location_city):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text_keyboards.change_name, callback_data=f'change_name_{key_id}')],
            [InlineKeyboardButton(text=text_keyboards.change_location, callback_data=f'change_location_{location_city}_{key_id}')],
            [InlineKeyboardButton(text=text_keyboards.recreate_key, callback_data=f'recreate_key_{key_id}')],
            [InlineKeyboardButton(text=text_keyboards.subscription_continue, callback_data=f'subscription_continue_{key_id}')],
            [InlineKeyboardButton(text=text_keyboards.go_back, callback_data=f'go_back_from_key_settings')]
        ]
    )
    return keyboard

def subscription_continue(key_id):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text_keyboards.buy_key_1_month, callback_data=f'continue_1_{key_id}')],
            [InlineKeyboardButton(text=text_keyboards.buy_key_3_months, callback_data=f'continue_3_{key_id}')],
            [InlineKeyboardButton(text=text_keyboards.buy_key_6_months, callback_data=f'continue_6_{key_id}')],
            [InlineKeyboardButton(text=text_keyboards.buy_key_12_months, callback_data=f'continue_12_{key_id}')],
            [InlineKeyboardButton(text=text_keyboards.go_back, callback_data=f'key_id_{key_id}')]
        ]
    )
    return keyboard

def admin_panel():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text_keyboards.admin_panel_add_server, callback_data='add_server')],
            [InlineKeyboardButton(text=text_keyboards.admin_close, callback_data='close')]
        ]
    )
    return keyboard

def add_key():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text_keyboards.add_key, callback_data='add_key')]
        ]
    )
    return keyboard

async def change_location(key_id, current_location_city):
    servers = await get_servers(current_location_city)
    
    builder = InlineKeyboardBuilder()
    for location in servers: 
        builder.add(
            InlineKeyboardButton(text=f'{location[0]}, {location[1]}', callback_data=f'set_location_{location[0]}_{key_id}')
        )
    builder.add(
        InlineKeyboardButton(text=text_keyboards.go_back, callback_data=f'key_id_{key_id}')
    )
    builder.adjust(1)
    keyboard = builder.as_markup()
    return keyboard

def stop_change_name():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard = [
            [InlineKeyboardButton(text=text_keyboards.stop_change_name, callback_data='close')]
        ]
    )
    return keyboard