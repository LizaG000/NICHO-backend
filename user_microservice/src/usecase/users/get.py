from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import GetByIdGate
from src.application.schemas.users import UpdateUserSchema, UserSchema
from src.infra.postgres.tables import UserModel
from dataclasses import dataclass
from src.usecase.users.schemas import UpdateUserUscaseSchema

@dataclass(slots=True, frozen=True, kw_only=True)
class GetUserUsecase(Usecase[UpdateUserUscaseSchema, UserSchema]):
    session: AsyncSession
    get_user: GetByIdGate[UserModel, UUID, UserSchema]
    
    async def __call__(self, id: UUID) -> UserSchema:
        async with self.session.begin():
            return await self.get_user(id=id)
