from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from uuid import UUID
from fastapi import APIRouter, Query
from fastapi import status
from src.usecase.status.get import GetStatusUsecase
from src.application.schemas.status import StatusSchema

ROUTER = APIRouter(route_class=DishkaRoute, tags=["Status"])

@ROUTER.post('', status_code=status.HTTP_200_OK, response_model=StatusSchema)
async def get_status(
    usecase: FromDishka[GetStatusUsecase],
    data: None) -> list[StatusSchema]:
    return await usecase(data=data)
