from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import GetAllByIdUserGate
from src.application.schemas.favorites import FavoriteSchema, CreateFavoriteSchema
from src.infra.postgres.tables import FavoritesModel
from dataclasses import dataclass
from src.application.schemas.auth import AuthSchema
from src.application.schemas.common import PaginationSchema


@dataclass(slots=True, frozen=True, kw_only=True)
class GetUserUsecase(Usecase[PaginationSchema, None]):
    session: AsyncSession
    auth: AuthSchema
    get_favorites: GetAllByIdUserGate[FavoritesModel, FavoriteSchema, UUID]

    async def __call__(self, data: PaginationSchema) -> None:
        async with self.session.begin():
            favorites =  await self.get_favorites(id_user=self.auth.sub)

