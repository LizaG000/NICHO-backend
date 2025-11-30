from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import GetByIdGate
from src.application.schemas.users import UserSchema
from src.infra.postgres.tables import UserModel
from dataclasses import dataclass
from src.application.schemas.auth import AuthSchema
from src.application.errors import ForbiddenError

@dataclass(slots=True, frozen=True, kw_only=True)
class GetUserUsecase(Usecase[None, UserSchema]):
    session: AsyncSession
    auth: AuthSchema
    get_user: GetByIdGate[UserModel, UUID, UserSchema]
    
    async def __call__(self, id: None = None) -> UserSchema:
        async with self.session.begin():
            if self.auth.role == 1:
                raise ForbiddenError("Customer или Admin", "Designer")
            return await self.get_user(id=self.auth.sub)
