from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter, Query
from fastapi import status
from src.usecase.favorites.create import CreateFavoritesUsecase
from src.usecase.favorites.get import GetFavoritesUsecase
from src.application.schemas.favorites import FavoriteSchema
from src.application.schemas.common import PaginationSchema
from src.usecase.favorites.schemas import GetCreateFavoritesSchema

ROUTER = APIRouter(route_class=DishkaRoute, tags=["Favorites"])

@ROUTER.post('', status_code=status.HTTP_200_OK)
async def create_favorites(
    usecase: FromDishka[CreateFavoritesUsecase],
    data: GetCreateFavoritesSchema) -> FavoriteSchema:
    return await usecase(data=data)

@ROUTER.get('', status_code=status.HTTP_200_OK)
async def get_favorites(
    usecase: FromDishka[GetFavoritesUsecase],
    data: PaginationSchema = Query()) -> None:
    await usecase(data=data)