from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter
from fastapi import status
from src.usecase.favorites.create import CreateFavoritesUsecase
from src.usecase.favorites.schemas import GetCreateFavoritesSchema

ROUTER = APIRouter(route_class=DishkaRoute, tags=["Favorites"])

@ROUTER.post('', status_code=status.HTTP_200_OK)
async def create_users(
    usecase: FromDishka[CreateFavoritesUsecase],
    data: GetCreateFavoritesSchema) -> None:
    await usecase(data=data)