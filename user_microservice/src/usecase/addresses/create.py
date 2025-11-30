from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import CreateReturningGate
from src.infra.postgres.gateways.address import GetAddressGate
from src.application.schemas.addresses import CreateAddressSchema, AddressSchema
from src.infra.postgres.tables import AddressesModel
from dataclasses import dataclass
from loguru import logger
from src.application.schemas.auth import AuthSchema
from src.application.errors import ForbiddenError, UnauthorizedError


@dataclass(slots=True, frozen=True, kw_only=True)
class CreateAddressUsecase(Usecase[CreateAddressSchema, AddressSchema]):
    session: AsyncSession
    auth: AuthSchema
    create_address: CreateReturningGate[AddressesModel, CreateAddressSchema, AddressSchema]
    get_address: GetAddressGate

    async def __call__(self, data: CreateAddressSchema) -> AddressSchema:
        async with self.session.begin():
            if self.auth.role == 1:
                raise ForbiddenError("Customer или Admin", "Designer")
            address = await self.get_address(data)
            if address is not None:
                return address
            return await self.create_address(data)
