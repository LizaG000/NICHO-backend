from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import CreateReturningGate
from src.infra.postgres.tables import BasketModel
from src.application.schemas.baskets import BasketSchema, CreateBasketSchema
from dataclasses import dataclass
from src.application.schemas.auth import AuthSchema
from src.application.errors import ForbiddenError


@dataclass(slots=True, frozen=True, kw_only=True)
class CreateBasketUsecase(Usecase[CreateBasketSchema, BasketSchema]):
    session: AsyncSession
    auth: AuthSchema
    create_favorites: CreateReturningGate[BasketModel, CreateBasketSchema, BasketSchema]

    async def __call__(self, data: CreateBasketSchema) -> BasketSchema:
        async with self.session.begin():
            if self.auth.role == 1:
                raise ForbiddenError("Customer или Admin", "Designer")
            return await self.create_favorites(data)