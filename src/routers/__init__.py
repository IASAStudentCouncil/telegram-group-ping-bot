from aiogram import Router
from .private_commands import router as private_commands_router
from .group_commands import router as group_commands_router

# Initialize the main router for handling all bot commands
main_router = Router(name=__name__)

# Include routers from different modules
main_router.include_routers(
    private_commands_router,
    group_commands_router
)

__all__ = ("main_router",)
