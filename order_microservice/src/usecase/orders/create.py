from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import CreateReturningGate
from src.infra.postgres.gateways.status import GetStatusGate
from dataclasses import dataclass
from src.usecase.orders.schemas import GetCreateOrderSchema, ReturnOrderSchema
from src.infra.postgres.tables import OrdersProductsModel, OrdersModel, StatusModel
from src.application.schemas.orders import CreateOrderSchema, OrderSchema
from src.application.schemas.order_products import CreateOrderProductSchema, OrderProductSchema
from src.application.schemas.auth import AuthSchema


@dataclass(slots=True, frozen=True, kw_only=True)
class CreateOrderUsecase(Usecase[GetCreateOrderSchema, ReturnOrderSchema]):
    session: AsyncSession
    auth: AuthSchema
    create_order: CreateReturningGate[OrdersModel, CreateOrderSchema, OrderSchema]
    create_order_product: CreateReturningGate[OrdersProductsModel, CreateOrderProductSchema, OrderProductSchema]
    get_status: GetStatusGate

    async def __call__(self, data: GetCreateOrderSchema) -> ReturnOrderSchema:
        async with self.session.begin():
            status = await self.get_status(data.status)
            price = 0
            for product in data.products:
                price += product.price*product.count
            order = await self.create_order(CreateOrderSchema(
                id_user=self.auth.sub,
                id_address=data.id_address,
                id_status=status.id,
                price=price
            ))
            products = []
            for product in data.products:
                item = await self.create_order_product(
                    CreateOrderProductSchema(
                        id_order=order.id,
                        id_product=product.id_product,
                        count=product.count,
                        size=product.size,
                        price=product.price,
                        discount=product.discount
                    )
                )

                products.append(item)

            return ReturnOrderSchema(
                id=order.id,
                id_user=order.id_user,
                id_address=order.id_address,
                status=data.status,
                price=price,
                created_at=order.created_at,
                updated_at=order.updated_at,
                products=products
            )


