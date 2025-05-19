from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

import os
from dotenv import load_dotenv


load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))