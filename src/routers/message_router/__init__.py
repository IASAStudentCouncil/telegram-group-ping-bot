from aiogram import Router

from .group_messages import router as group_messages_router
from .private_messages import router as private_messages_router

# Commands router for handling all bot commands
message_router = Router(name=__name__)
message_router.include_routers(
    private_messages_router,
    group_messages_router
)

__all__ = ("message_router",)
