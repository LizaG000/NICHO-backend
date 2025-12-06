from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from uuid import UUID
from src.infra.postgres.gateways.base import DeleteReturningGate
from src.infra.postgres.tables import BasketModel
from src.application.schemas.baskets import BasketSchema
from dataclasses import dataclass
from src.application.schemas.auth import AuthSchema
from src.application.errors import ForbiddenError


@dataclass(slots=True, frozen=True, kw_only=True)
class DeleteBasketUsecase(Usecase[UUID, BasketSchema]):
    session: AsyncSession
    auth: AuthSchema
    delete_basket: DeleteReturningGate[BasketModel, UUID, BasketSchema]

    async def __call__(self, data: UUID) -> BasketSchema:
        async with self.session.begin():
            if self.auth.role == 1:
                raise ForbiddenError("Customer или Admin", "Designer")
            return await self.delete_basket(data)