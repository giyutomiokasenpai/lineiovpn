import asyncio

from main.bot import bot
from texts import text_messages
from keyboards import inline_keyboards

async def broadcast_deleted(user_id):
    try:
        await bot.send_message(
            chat_id=user_id, 
            text=text_messages.broadcast_deleting, 
            reply_markup=inline_keyboards.buy_key()
        )
        await asyncio.sleep(0.05)
    except Exception as e:
        print(f'Error broadcasting: {e}')

async def broadcast_continue_broadcast(user_id, duration):
    try:
        text = f'{text_messages.broadcast_continue_one} {duration} {text_messages.broadcast_continue_two if duration != 1 else text_messages.broadcast_continue_two_1}'
        await bot.send_message(
            chat_id=user_id,
            text=text
        )
    except Exception as e:
        print(f'Error broadcasting: {e}')