from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import UpdateReturningGate
from src.application.schemas.users import UpdateUserSchema, UserSchema
from src.infra.postgres.tables import UserModel
from dataclasses import dataclass
from src.usecase.users.schemas import UpdateUserUscaseSchema

@dataclass(slots=True, frozen=True, kw_only=True)
class UpdateUserUsecase(Usecase[UpdateUserUscaseSchema, UserSchema]):
    session: AsyncSession
    update_user: UpdateReturningGate[UserModel, UpdateUserSchema, UUID, UserSchema]
    
    async def __call__(self, data: UpdateUserUscaseSchema) -> UserSchema:
        async with self.session.begin():
            return await self.update_user(data.id, data.user)
