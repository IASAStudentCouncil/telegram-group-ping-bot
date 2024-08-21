from aiogram import Router
from .message_routers import message_router
from .callback_routers import callback_router

# Main router that handles everything
main_router = Router(name=__name__)
main_router.include_routers(
    message_router,
    callback_router
)

__all__ = ("main_router",)
