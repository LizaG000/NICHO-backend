from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from src.presentation.fastapi.routes.core.users.api import ROUTER as USER_ROUTER
from src.presentation.fastapi.routes.core.addresses.api import ROUTER as ADDRESSES_ROUTER
from src.presentation.fastapi.routes.core.favorites.api import ROUTER as FAVORITES_ROUTER
from src.presentation.fastapi.routes.core.baskets.api import ROUTER as BASKETS_ROUTER

def setup_core_router() -> APIRouter:
    router = APIRouter(route_class=DishkaRoute)

    router.include_router(prefix='/user', router=USER_ROUTER)
    router.include_router(prefix='/address', router=ADDRESSES_ROUTER)
    router.include_router(prefix='/favorites', router=FAVORITES_ROUTER)
    router.include_router(prefix='/baskets', router=BASKETS_ROUTER)
    return router
