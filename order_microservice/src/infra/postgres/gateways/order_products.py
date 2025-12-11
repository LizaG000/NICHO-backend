from dataclasses import dataclass
from loguru import logger
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.infra.postgres.tables import OrdersProductsModel
from src.application.schemas.order_products import OrderProductSchema


@dataclass(slots=True, kw_only=True)
class PostgresGateway:
    session: AsyncSession


@dataclass(slots=True, kw_only=True)
class GetProductsAllGate(PostgresGateway):

    async def __call__(self, id_order: UUID) -> list[OrderProductSchema]:
        stmt = (select(
            OrdersProductsModel.id,
            OrdersProductsModel.id_order,
            OrdersProductsModel.id_product,
            OrdersProductsModel.count,
            OrdersProductsModel.size,
            OrdersProductsModel.price,
            OrdersProductsModel.discount,
            OrdersProductsModel.created_at,
            OrdersProductsModel.updated_at,
        ).where(OrdersProductsModel.id_order==id_order)
        .order_by(OrdersProductsModel.created_at.desc()))

        results = (await self.session.execute(stmt)).mappings().fetchall()
        logger.info(results)
        return [OrderProductSchema.model_validate(result) for result in results]

