from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from uuid import UUID
from fastapi import APIRouter, Query
from fastapi import status
from src.usecase.orders.create import CreateOrderUsecase
from src.usecase.orders.schemas import GetCreateOrderSchema, ReturnOrderSchema
from src.application.schemas.common import PaginationSchema
from src.usecase.orders.schemas import ReturnOrdersPagination
from src.usecase.orders.get_all import GetAllOrderUsecase

from src.usecase.orders.schemas import ReturnAllOrdersSchemas
from src.usecase.orders.get import GetOrderUsecase

ROUTER = APIRouter(route_class=DishkaRoute, tags=["Users"])

@ROUTER.post('', status_code=status.HTTP_200_OK, response_model=GetCreateOrderSchema)
async def create_users(
    usecase: FromDishka[CreateOrderUsecase],
    data: GetCreateOrderSchema) -> ReturnOrderSchema:
    return await usecase(data=data)


@ROUTER.get('/all', status_code=status.HTTP_200_OK, response_model=ReturnOrdersPagination)
async def create_users(
    usecase: FromDishka[GetAllOrderUsecase],
    data: PaginationSchema = Query()) -> ReturnOrdersPagination:
    return await usecase(data=data)


@ROUTER.get('', status_code=status.HTTP_200_OK, response_model=ReturnOrdersPagination)
async def create_users(
    usecase: FromDishka[GetOrderUsecase],
    id_order: UUID = Query()) -> ReturnAllOrdersSchemas:
    return await usecase(data=id_order)



