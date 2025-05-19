from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from fsm_machine.admin.add_server import ServerData
from texts import text_messages
from database.admin.insert_server import insert_server

router = Router()

@router.message(ServerData.api_url)
async def set_api_url(message: Message, state: FSMContext):
    await state.update_data(api_url=message.text)
    await message.answer(
        text=text_messages.insert_ip
    )
    await state.set_state(ServerData.ip)

@router.message(ServerData.ip)
async def set_api_url(message: Message, state: FSMContext):
    await state.update_data(ip=message.text)
    await message.answer(
        text=text_messages.insert_password
    )
    await state.set_state(ServerData.password)

@router.message(ServerData.password)
async def set_api_url(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    await message.answer(
        text=text_messages.insert_location_country
    )
    await state.set_state(ServerData.location_country)

@router.message(ServerData.location_country)
async def set_api_url(message: Message, state: FSMContext):
    await state.update_data(location_country=message.text)
    await message.answer(
        text=text_messages.insert_location_city
    )
    await state.set_state(ServerData.location_city)

@router.message(ServerData.location_city)
async def set_api_url(message: Message, state: FSMContext):
    await state.update_data(location_city=message.text)

    data = await state.get_data()
    api_url = data.get('api_url')
    ip = data.get('ip')
    password = data.get('password')
    location_country = data.get('location_country')
    location_city = data.get('location_city')
    await insert_server(api_url, ip, password, location_country, location_city)

    await message.answer(
        text=text_messages.server_done
    )
    await state.clear()