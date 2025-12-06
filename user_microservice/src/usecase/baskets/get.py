import httpx
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import GetAllByIdUserGate
from src.application.schemas.baskets import BasketSchema
from src.infra.postgres.tables import BasketModel
from dataclasses import dataclass
from src.application.schemas.auth import AuthSchema
from src.application.schemas.common import PaginationSchema
from loguru import logger
from src.usecase.favorites.schemas import ReturnProductSchema, ReturnPaginationSchema


@dataclass(slots=True, frozen=True, kw_only=True)
class GetBasketUsecase(Usecase[PaginationSchema, ReturnPaginationSchema]):
    session: AsyncSession
    auth: AuthSchema
    get_baskets: GetAllByIdUserGate[BasketModel, BasketSchema, UUID]

    async def __call__(self, data: PaginationSchema) -> ReturnPaginationSchema:
        async with self.session.begin():
            baskets =  await self.get_baskets(id_user=self.auth.sub)
            async with httpx.AsyncClient(timeout=30.0) as client:
                params = { "ids": [str(baskets[i].id_product) for i in range(data.offset, min(data.offset+data.limit, len(baskets)))]}
                responses = await client.post("http://nicho-designer.tw1.ru/subproducts/get-by-id-list", json=params)
                r = responses.json()
                logger.info(r)
                items = [ReturnProductSchema.model_validate(response) for response in r]
                for i in range(0, len(items)):
                    items[i].subProductSizes = baskets[i+data.offset].size
                    items[i].productId = baskets[i+data.offset].id
                print(items[0])
                return ReturnPaginationSchema(
                    count=len(baskets),
                    items=items)


