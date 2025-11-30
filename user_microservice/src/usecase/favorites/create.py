from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import CreateReturningGate
from src.infra.postgres.tables import FavoritesModel
from src.application.schemas.favorites import FavoriteSchema, CreateFavoriteSchema
from dataclasses import dataclass
from src.application.schemas.auth import AuthSchema
from src.application.errors import ForbiddenError, UnauthorizedError
from src.usecase.favorites.schemas import GetCreateFavoritesSchema


@dataclass(slots=True, frozen=True, kw_only=True)
class CreateFavoritesUsecase(Usecase[GetCreateFavoritesSchema, FavoriteSchema]):
    session: AsyncSession
    auth: AuthSchema
    create_favorites: CreateReturningGate[FavoritesModel, CreateFavoriteSchema, FavoriteSchema]

    async def __call__(self, data: GetCreateFavoritesSchema) -> FavoriteSchema:
        async with self.session.begin():
            if self.auth.role == 1:
                raise ForbiddenError("Customer или Admin", "Designer")
            elif data.id_user != self.auth.sub and self.auth.role != 2:
                raise UnauthorizedError()
            return await self.create_favorites(CreateFavoriteSchema(
                id_user=self.auth.sub,
                id_product=data.id_product
            ))