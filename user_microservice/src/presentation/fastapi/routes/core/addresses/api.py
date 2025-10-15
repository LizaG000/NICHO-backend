from uuid import UUID
from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter
from fastapi import status
from src.usecase.addresses.create import CreateAddressUsecase
from src.usecase.addresses.get_all import GetAddressesUsecase
from src.usecase.addresses.delete import DeleteAddressesUsecase
from src.application.schemas.addresses import CreateAddressSchema, AddressSchema

ROUTER = APIRouter(route_class=DishkaRoute, tags=["Addresses"])

@ROUTER.post('', status_code=status.HTTP_200_OK)
async def create_address(
    usecase: FromDishka[CreateAddressUsecase],
    address: CreateAddressSchema) -> AddressSchema:
    return await usecase(address)

@ROUTER.get('', status_code=status.HTTP_200_OK)
async def get_addresses_by_user(
    usecase: FromDishka[GetAddressesUsecase],
    id_user: UUID) -> list[AddressSchema]:
    return await usecase(id_user)


@ROUTER.delete('', status_code=status.HTTP_200_OK)
async def delete_address_by_user(
    usecase: FromDishka[DeleteAddressesUsecase],
    id: UUID) -> AddressSchema:
    return await usecase(id=id)