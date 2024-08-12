from aiogram import Router
from .command_router import router as command_router

main_router = Router(name=__name__)
main_router.include_routers(
    command_router
)

__all__ = ("main_router",)
