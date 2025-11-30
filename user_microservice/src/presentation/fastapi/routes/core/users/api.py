from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from uuid import UUID
from fastapi import APIRouter
from fastapi import status
from src.application.schemas.users import UserSchema
from src.usecase.users.create import CreateUserUsecase
from src.usecase.users.update import UpdateUserUsecase
from src.usecase.users.get import GetUserUsecase
from src.usecase.users.schemas import CreateUserSchema, UpdateUserSchema

ROUTER = APIRouter(route_class=DishkaRoute, tags=["Users"])

@ROUTER.post('', status_code=status.HTTP_200_OK)
async def create_users(
    usecase: FromDishka[CreateUserUsecase],
    user: CreateUserSchema) -> UserSchema:
    return await usecase(data=user)

@ROUTER.patch('', status_code=status.HTTP_200_OK)
async def update_users(
    usecase: FromDishka[UpdateUserUsecase],
    user: UpdateUserSchema) -> UserSchema:
    return await usecase(user)

@ROUTER.get('', status_code=status.HTTP_200_OK)
async def get_user(
    usecase: FromDishka[GetUserUsecase],) -> UserSchema:
    return await usecase()