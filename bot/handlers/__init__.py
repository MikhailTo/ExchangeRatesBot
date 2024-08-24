from aiogram import Router


def setup_routers() -> Router:
    from . import common
    from . import chosing_currencies
    
    router = Router()
    router.include_router(common.router)
    router.include_router(chosing_currencies.router)
    
    return router