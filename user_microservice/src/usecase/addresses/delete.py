from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import DeleteReturningGate
from src.application.schemas.addresses import AddressSchema
from src.infra.postgres.tables import AddressesModel
from dataclasses import dataclass
from src.application.schemas.auth import AuthSchema
from src.application.errors import ForbiddenError, UnauthorizedError

@dataclass(slots=True, frozen=True, kw_only=True)
class DeleteAddressesUsecase(Usecase[UUID, list[AddressSchema]]):
    session: AsyncSession
    auth: AuthSchema
    delete_address: DeleteReturningGate[AddressesModel, UUID,AddressSchema]
    
    async def __call__(self, id: UUID) -> AddressSchema:
        async with self.session.begin():
            if self.auth.role == 1:
                raise ForbiddenError("Customer или Admin", "Designer")
            return await self.delete_address(entity_id=id)
