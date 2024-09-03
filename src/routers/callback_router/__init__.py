from aiogram import Router
from .private_callbacks import router as private_callbacks_router
from .group_callbacks import router as group_callbacks_router

# Commands router for handling all callbacks
callback_router = Router(name=__name__)
callback_router.include_routers(
    private_callbacks_router,
    group_callbacks_router
)

__all__ = ("callback_router",)
