from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import GetAllByIdUserGate
from src.application.schemas.addresses import AddressSchema
from src.infra.postgres.tables import AddressesModel
from dataclasses import dataclass
from src.application.schemas.auth import AuthSchema
from src.application.errors import ForbiddenError, UnauthorizedError

@dataclass(slots=True, frozen=True, kw_only=True)
class GetAddressesUsecase(Usecase[None, list[AddressSchema]]):
    session: AsyncSession
    auth: AuthSchema
    get_addresses: GetAllByIdUserGate[AddressesModel, AddressSchema, UUID]
    
    async def __call__(self, id_user: None = None) -> list[AddressSchema]:
        async with self.session.begin():
            if self.auth.role == 1:
                raise ForbiddenError("Customer или Admin", "Designer")
            return await self.get_addresses(self.auth.sub)
