from aiogram import Router
from .private_commands import router as private_commands_router
from .group_commands import router as group_commands_router

# Commands router for handling all bot commands
commands_router = Router(name=__name__)
commands_router.include_routers(
    private_commands_router,
    group_commands_router
)

__all__ = ("commands_router",)
