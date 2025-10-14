from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter
from fastapi import status
from src.usecase.addresses.create import CreateAddressUsecase
from src.application.schemas.addresses import CreateAddressSchema, AddressSchema

ROUTER = APIRouter(route_class=DishkaRoute)

@ROUTER.post('', status_code=status.HTTP_200_OK)
async def create_address(
    usecase: FromDishka[CreateAddressUsecase],
    address: CreateAddressSchema) -> AddressSchema:
    return await usecase(address)
