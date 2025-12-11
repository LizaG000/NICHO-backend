from dataclasses import dataclass
from loguru import logger
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.infra.postgres.tables import StatusModel, OrdersModel
from src.application.errors import NotFoundError
from src.usecase.orders.schemas import ReturnAllOrders


@dataclass(slots=True, kw_only=True)
class PostgresGateway:
    session: AsyncSession


@dataclass(slots=True, kw_only=True)
class GetOrdersAllGate(PostgresGateway):

    async def __call__(self, id_user: UUID) -> list[ReturnAllOrders]:
        stmt = (select(
            OrdersModel.id,
            OrdersModel.id_user,
            OrdersModel.id_designer,
            OrdersModel.id_addresses.label("address"),
            OrdersModel.price,
            StatusModel.status,
            OrdersModel.created_at
        ).join(OrdersModel, OrdersModel.id_status==StatusModel.id)
        .where((OrdersModel.id_user == id_user) |
            (OrdersModel.id_designer == id_user))
        .group_by(
            OrdersModel.id,
            OrdersModel.id_user,
            OrdersModel.id_designer,
            OrdersModel.id_addresses.label("address"),
            OrdersModel.price,
            StatusModel.status,
            OrdersModel.created_at,
        )).order_by(OrdersModel.created_at.desc())
        results = (await self.session.execute(stmt)).mappings().fetchall()
        logger.info(results)
        return [ReturnAllOrders.model_validate(result) for result in results]


@dataclass(slots=True, kw_only=True)
class GetOrderGate(PostgresGateway):

    async def __call__(self, id_order: UUID) -> ReturnAllOrders | None:
        stmt = (select(
            OrdersModel.id,
            OrdersModel.id_user,
            OrdersModel.price,
            OrdersModel.id_addresses.label("address"),
            StatusModel.status,
            OrdersModel.created_at
        ).join(OrdersModel, OrdersModel.id_status==StatusModel.id)
        .where(OrdersModel.id==id_order)
        .group_by(
            OrdersModel.id,
            OrdersModel.id_user,
            OrdersModel.id_designer,
            OrdersModel.id_addresses.label("address"),
            OrdersModel.price,
            StatusModel.status,
            OrdersModel.created_at,
        ))
        result = (await self.session.execute(stmt)).mappings().fetchone()
        logger.info(result)
        if result is None:
            raise NotFoundError(OrdersModel.__tablename__)
        return ReturnAllOrders.model_validate(result)


