from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import DeleteReturningGate
from src.infra.postgres.tables import FavoritesModel
from src.application.schemas.favorites import FavoriteSchema
from dataclasses import dataclass
from src.application.schemas.auth import AuthSchema
from src.application.errors import ForbiddenError
from src.usecase.favorites.schemas import GetCreateFavoritesSchema


@dataclass(slots=True, frozen=True, kw_only=True)
class DeleteFavoritesUsecase(Usecase[UUID, FavoriteSchema]):
    session: AsyncSession
    auth: AuthSchema
    delete_favorites: DeleteReturningGate[FavoritesModel, UUID, FavoriteSchema]

    async def __call__(self, data: UUID) -> FavoriteSchema:
        async with self.session.begin():
            if self.auth.role == 1:
                raise ForbiddenError("Customer или Admin", "Designer")
            return await self.delete_favorites(data)