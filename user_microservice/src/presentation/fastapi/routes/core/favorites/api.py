from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter, Query
from uuid import UUID
from fastapi import status
from src.usecase.favorites.create import CreateFavoritesUsecase
from src.usecase.favorites.delete import DeleteFavoritesUsecase
from src.usecase.favorites.get import GetFavoritesUsecase
from src.application.schemas.favorites import FavoriteSchema
from src.application.schemas.common import PaginationSchema
from src.usecase.favorites.schemas import GetCreateFavoritesSchema
from src.usecase.favorites.schemas import ReturnPaginationSchema

ROUTER = APIRouter(route_class=DishkaRoute, tags=["Favorites"])

@ROUTER.post('', status_code=status.HTTP_200_OK, response_model=FavoriteSchema)
async def create_favorites(
    usecase: FromDishka[CreateFavoritesUsecase],
    data: GetCreateFavoritesSchema) -> FavoriteSchema:
    return await usecase(data=data)

@ROUTER.get('', status_code=status.HTTP_200_OK, response_model=ReturnPaginationSchema)
async def get_favorites(
    usecase: FromDishka[GetFavoritesUsecase],
    data: PaginationSchema = Query()) -> ReturnPaginationSchema:
    return await usecase(data=data)


@ROUTER.delete('', status_code=status.HTTP_200_OK, response_model=FavoriteSchema)
async def delete_favorites(
    usecase: FromDishka[DeleteFavoritesUsecase],
    data: UUID) -> FavoriteSchema:
    return await usecase(data=data)