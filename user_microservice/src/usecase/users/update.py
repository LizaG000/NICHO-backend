from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import UpdateReturningGate
from src.application.schemas.users import UpdateUserSchema, UserSchema
from src.infra.postgres.tables import UserModel
from dataclasses import dataclass
from src.application.schemas.auth import AuthSchema
from src.application.errors import ForbiddenError, UnauthorizedError

@dataclass(slots=True, frozen=True, kw_only=True)
class UpdateUserUsecase(Usecase[UpdateUserSchema, UserSchema]):
    session: AsyncSession
    auth: AuthSchema
    update_user: UpdateReturningGate[UserModel, UpdateUserSchema, UUID, UserSchema]
    
    async def __call__(self, data: UpdateUserSchema) -> UserSchema:
        async with self.session.begin():
            if self.auth.role == 1:
                raise ForbiddenError("Customer или Admin", "Designer")
            return await self.update_user(self.auth.sub, data.user)
