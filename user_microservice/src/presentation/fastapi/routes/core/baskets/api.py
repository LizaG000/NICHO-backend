from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter, Query
from uuid import UUID
from fastapi import status
from src.application.schemas.baskets import CreateBasketSchema, BasketSchema, UpdateBasketSchema
from src.usecase.baskets.create import CreateBasketUsecase
from src.usecase.baskets.update import UpdateBasketUsecase
from src.usecase.baskets.delete import DeleteBasketUsecase
from src.usecase.baskets.get import GetBasketUsecase
from src.usecase.favorites.schemas import ReturnPaginationSchema
from src.application.schemas.common import PaginationSchema

ROUTER = APIRouter(route_class=DishkaRoute, tags=["Baskets"])

@ROUTER.post('', status_code=status.HTTP_200_OK, response_model=BasketSchema)
async def create_basket(
    usecase: FromDishka[CreateBasketUsecase],
    data: CreateBasketSchema) -> BasketSchema:
    return await usecase(data=data)

@ROUTER.put('', status_code=status.HTTP_200_OK, response_model=BasketSchema)
async def update_basket(
    usecase: FromDishka[UpdateBasketUsecase],
    data: UpdateBasketSchema) -> BasketSchema:
    return await usecase(data=data)

@ROUTER.delete('', status_code=status.HTTP_200_OK, response_model=BasketSchema)
async def delete_basket(
    usecase: FromDishka[DeleteBasketUsecase],
    data: UUID) -> BasketSchema:
    return await usecase(data=data)


@ROUTER.get('', status_code=status.HTTP_200_OK, response_model=ReturnPaginationSchema)
async def get_favorites(
    usecase: FromDishka[GetBasketUsecase],
    data: PaginationSchema = Query()) -> ReturnPaginationSchema:
    return await usecase(data=data)
