from aiogram import Router

from handlers.admin import callbacks_admin, messages_admin, commands_admin
from handlers.user import callbacks, messages, commands


def setup_routers() -> Router:
    main_router = Router()

    main_router.include_router(commands.router)
    main_router.include_router(messages.router)
    main_router.include_router(callbacks.router)
    main_router.include_router(commands_admin.router)
    main_router.include_router(messages_admin.router)
    main_router.include_router(callbacks_admin.router)
    return main_router