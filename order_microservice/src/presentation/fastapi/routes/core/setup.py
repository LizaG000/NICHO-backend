from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from src.presentation.fastapi.routes.core.orders.api import ROUTER as ORDERS_ROUTER
from src.presentation.fastapi.routes.core.status.api import ROUTER as STATUS_ROUTER

def setup_core_router() -> APIRouter:
    router = APIRouter(route_class=DishkaRoute)

    router.include_router(prefix='/orders', router=ORDERS_ROUTER)
    router.include_router(prefix='/status', router=STATUS_ROUTER)
    return router
