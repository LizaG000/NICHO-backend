import httpx
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import GetAllByIdUserGate
from src.application.schemas.favorites import FavoriteSchema
from src.infra.postgres.tables import FavoritesModel
from dataclasses import dataclass
from src.application.schemas.auth import AuthSchema
from src.application.schemas.common import PaginationSchema
from loguru import logger
from src.usecase.favorites.schemas import ReturnProductSchema, ReturnPaginationSchema


@dataclass(slots=True, frozen=True, kw_only=True)
class GetFavoritesUsecase(Usecase[PaginationSchema, ReturnPaginationSchema]):
    session: AsyncSession
    auth: AuthSchema
    get_favorites: GetAllByIdUserGate[FavoritesModel, FavoriteSchema, UUID]

    async def __call__(self, data: PaginationSchema) -> ReturnPaginationSchema:
        async with self.session.begin():
            favorites =  await self.get_favorites(id_user=self.auth.sub)
            async with httpx.AsyncClient(timeout=30.0) as client:
                params = { "ids": [str(favorites[i].id_product) for i in range(data.offset, min(data.offset+data.limit, len(favorites)))]}
                responses = await client.post("http://nicho-designer.tw1.ru/subproducts/get-by-id-list", json=params)
                r = responses.json()
                logger.info(r)
                items = [ReturnProductSchema.model_validate(response) for response in r]
                for i in range(0, len(items)):
                    items[i].subProductSizes = favorites[i+data.offset].size
                    items[i].productId = favorites[i+data.offset].id
                print(items[0])
                return ReturnPaginationSchema(
                    count=len(favorites),
                    items=items)


