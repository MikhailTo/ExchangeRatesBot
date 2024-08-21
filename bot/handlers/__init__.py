from aiogram import Router


def setup_routers() -> Router:
    from . import commands

    router = Router()
    router.include_router(commands.router)

    return router