from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from uuid import UUID
from src.infra.postgres.gateways.base import UpdateReturningGate
from dataclasses import dataclass
from src.application.schemas.orders import OrderSchema, UpdateOrderSchema
from src.usecase.orders.schemas import GetUpdateOrderSchema
from src.infra.postgres.tables import OrdersModel
from src.application.schemas.auth import AuthSchema


@dataclass(slots=True, frozen=True, kw_only=True)
class UpdateOrderUsecase(Usecase[GetUpdateOrderSchema, OrderSchema]):
    session: AsyncSession
    auth: AuthSchema
    update_order: UpdateReturningGate[OrdersModel, UpdateOrderSchema, UUID, OrderSchema]

    async def __call__(self, data: GetUpdateOrderSchema) -> OrderSchema:
        async with self.session.begin():
            return await self.update_order(entity_id=data.id, entity=UpdateOrderSchema(
                id_status=data.id_status,
                updated_at=data.updated_at
            ))
