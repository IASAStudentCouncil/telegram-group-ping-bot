from aiogram import Router
from .message_router import message_router
from .callback_router import callback_router
from .admin_router import router as admin_router

main_router = Router(name=__name__)     # Main router that handles everything
main_router.include_routers(
    message_router,
    callback_router,
    admin_router
)

__all__ = ("main_router",)
