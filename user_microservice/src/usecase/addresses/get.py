from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from uuid import UUID
from src.infra.postgres.gateways.base import GetByIdGate
from src.application.schemas.addresses import AddressSchema
from src.infra.postgres.tables import AddressesModel
from dataclasses import dataclass
from src.application.schemas.auth import AuthSchema
from src.application.errors import ForbiddenError


@dataclass(slots=True, frozen=True, kw_only=True)
class GetAddressUsecase(Usecase[UUID, AddressSchema]):
    session: AsyncSession
    auth: AuthSchema
    get_address: GetByIdGate[AddressesModel, UUID, AddressSchema]

    async def __call__(self, data: UUID) -> AddressSchema:
        async with self.session.begin():
            if self.auth.role == 1:
                raise ForbiddenError("Customer или Admin", "Designer")
            return await self.get_address(data)
