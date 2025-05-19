import asyncio

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage 

from router.routers import setup_routers
from main.bot import bot
from scheduler.delete_subscription import start_scheduler

dp = Dispatcher(storage=MemoryStorage())
dp.include_router(setup_routers())

async def main():
    start_scheduler()
    await dp.start_polling(bot, skip_updates=True)

if __name__ == '__main__':
    asyncio.run(main())