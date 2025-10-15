from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import DeleteReturningGate
from src.application.schemas.addresses import AddressSchema
from src.infra.postgres.tables import AddressesModel
from dataclasses import dataclass

@dataclass(slots=True, frozen=True, kw_only=True)
class DeleteAddressesUsecase(Usecase[UUID, list[AddressSchema]]):
    session: AsyncSession
    delete_address: DeleteReturningGate[AddressesModel, UUID,AddressSchema]
    
    async def __call__(self, id: UUID) -> AddressSchema:
        async with self.session.begin():
            return await self.delete_address(entity_id=id)
