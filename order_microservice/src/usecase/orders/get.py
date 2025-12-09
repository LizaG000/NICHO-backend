from http.client import responses

import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from uuid import UUID
from src.infra.postgres.gateways.orders import GetOrderGate
from src.infra.postgres.gateways.order_products import GetProductsAllGate
from src.application.schemas.common import PaginationSchema
from src.usecase.orders.schemas import ReturnProductSchema, AddressSchema, ReturnProduct, ReturnAllOrdersSchemas
from dataclasses import dataclass
from src.application.schemas.auth import AuthSchema


@dataclass(slots=True, frozen=True, kw_only=True)
class GetOrderUsecase(Usecase[PaginationSchema, ReturnAllOrdersSchemas]):
    session: AsyncSession
    auth: AuthSchema
    get_order: GetOrderGate
    get_products: GetProductsAllGate

    async def __call__(self, data: UUID) -> ReturnAllOrdersSchemas:
        async with self.session.begin():
            order = await self.get_order(self.auth.sub)
            orders_products = await self.get_products(order.id)
            id_products = [str(product.id_product) for product in orders_products]
            async with httpx.AsyncClient(timeout=30.0) as client:
                products = await client.post("http://nicho-designer.tw1.ru/subproducts/get-by-id-list", json=id_products)
                r = products.json()
                items = [ReturnProductSchema.model_validate(product) for product in r]
                address = await client.get(f"http://nicho-user-micro.tw1.ru:8001/address?id_address={order.address}",)
                address = address.json()
                address =AddressSchema.model_validate(address)
                response = [ReturnProduct(
                    id=items[i].id,
                    id_product=items[i].id_products,
                    id_order=order.id,
                    price=orders_products[i].price,
                    count=orders_products[i].count,
                    size=orders_products[i].size,
                    discount=orders_products[i].discount,
                    photos=items[i].photos,
                    color=items[i].color,
                    created_at=orders_products[i].created_at,
                    updated_at=orders_products[i].updated_at,
                ) for i in range(len(items))]

                return ReturnAllOrdersSchemas(
                    id=order.id,
                    id_user=self.auth.sub,
                    address=address,
                    price=order.price,
                    status=order.status,
                    created_at=order.created_at,
                    products=response,
                )






