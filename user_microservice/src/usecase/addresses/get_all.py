from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import GetAllByIdUserGate
from src.application.schemas.addresses import AddressSchema
from src.infra.postgres.tables import AddressesModel
from dataclasses import dataclass

@dataclass(slots=True, frozen=True, kw_only=True)
class GetAddressesUsecase(Usecase[UUID, list[AddressSchema]]):
    session: AsyncSession
    get_addresses: GetAllByIdUserGate[AddressesModel, AddressSchema, UUID]
    
    async def __call__(self, id_user: UUID) -> list[AddressSchema]:
        async with self.session.begin():
            return await self.get_addresses(id_user)
