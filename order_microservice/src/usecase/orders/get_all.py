from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.postgres.gateways.orders import GetOrdersAllGate
from src.application.schemas.common import PaginationSchema
from src.usecase.orders.schemas import ReturnOrdersPagination
from dataclasses import dataclass
from src.application.schemas.auth import AuthSchema
from src.application.errors import NotFoundError
from src.infra.postgres.tables import OrdersModel


@dataclass(slots=True, frozen=True, kw_only=True)
class GetAllOrderUsecase(Usecase[PaginationSchema, ReturnOrdersPagination]):
    session: AsyncSession
    auth: AuthSchema
    get_orders: GetOrdersAllGate

    async def __call__(self, data: PaginationSchema) -> ReturnOrdersPagination:
        async with self.session.begin():
            orders = await self.get_orders(self.auth.sub)
            if orders == []:
                raise NotFoundError(OrdersModel.__tablename__)
            _next = data.offset + data.limit
            if _next > len(orders):
                _next = _next-len(orders)
            response = orders[data.offset:next]
            if data.offset == 0:
                limit_left = None
                offset_left = None
            else:
                limit_left = data.limit
                offset_left = data.offset-data.limit

            if data.offset+data.limit == len(orders):
                limit_right = None
                offset_right = None
            else:
                offset_right = data.limit
                limit_right = data.offset+data.limit
            return ReturnOrdersPagination(
                orders=response,
                limit_left=limit_left,
                limit_right=limit_right,
                offset_right=offset_right,
                offset_left=offset_left,
                items=len(orders)
            )

