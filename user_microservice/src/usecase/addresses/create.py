from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import CreateReturningGate
from src.infra.postgres.gateways.address import GetAddressGate
from src.application.schemas.addresses import CreateAddressSchema, AddressSchema
from src.infra.postgres.tables import AddressesModel
from dataclasses import dataclass
from loguru import logger


@dataclass(slots=True, frozen=True, kw_only=True)
class CreateAddressUsecase(Usecase[CreateAddressSchema, AddressSchema]):
    session: AsyncSession
    create_user: CreateReturningGate[AddressesModel, CreateAddressSchema, AddressSchema]
    get_address: GetAddressGate

    async def __call__(self, data: CreateAddressSchema) -> AddressSchema:
        async with self.session.begin():
            logger.info(data)
            address = await self.get_address(data)
            logger.info(address)
            if address is not None:
                return address
            return await self.create_user(data)
