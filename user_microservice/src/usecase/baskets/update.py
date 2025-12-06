from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import UpdateReturningGate
from src.infra.postgres.tables import BasketModel
from src.application.schemas.baskets import BasketSchema, UpdateBasketSchema
from dataclasses import dataclass
from src.application.schemas.auth import AuthSchema
from src.application.errors import ForbiddenError


@dataclass(slots=True, frozen=True, kw_only=True)
class UpdateBasketUsecase(Usecase[UpdateBasketSchema, BasketSchema]):
    session: AsyncSession
    auth: AuthSchema
    update_basckets: UpdateReturningGate[BasketModel, UpdateBasketSchema, UUID, BasketSchema]

    async def __call__(self, data: UpdateBasketSchema) -> BasketSchema:
        async with self.session.begin():
            if self.auth.role == 1:
                raise ForbiddenError("Customer или Admin", "Designer")
            return await self.update_basckets(self.auth.sub, data)