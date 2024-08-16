from aiogram import Router
from .commands_routers import commands_router
from .callback_routers import callbacks_router

# Main router that handles everything
main_router = Router(name=__name__)
main_router.include_routers(
    commands_router,
    callbacks_router
)

__all__ = ("main_router",)
