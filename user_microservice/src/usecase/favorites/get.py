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


@dataclass(slots=True, frozen=True, kw_only=True)
class GetFavoritesUsecase(Usecase[PaginationSchema, None]):
    session: AsyncSession
    auth: AuthSchema
    get_favorites: GetAllByIdUserGate[FavoritesModel, FavoriteSchema, UUID]

    async def __call__(self, data: PaginationSchema) -> None:
        async with self.session.begin():
            favorites =  await self.get_favorites(id_user=self.auth.sub)
            async with httpx.AsyncClient(timeout=30.0) as client:
                params = { "ids": [str(favorites[i].id_product) for i in range(data.offset, data.offset+data.limit)]}
                logger.info(params)
                response = await client.post("http://nicho-designer.tw1.ru/subproducts/get-by-id-list", json=params)
                logger.info(response)
                logger.info(response.text)


