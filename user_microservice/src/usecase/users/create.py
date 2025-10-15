from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import CreateReturningGate
from src.application.schemas.users import CreateUserSchema, UserSchema
from src.infra.postgres.tables import UserModel
from dataclasses import dataclass
from src.infra.postgres.gateways.users import GetUserGate
from src.usecase.users.schemas import UserLoginSchemas
from src.application.errors import UserAlreadyExistsError

@dataclass(slots=True, frozen=True, kw_only=True)
class CreateUserUsecase(Usecase[CreateUserSchema, UserSchema]):
    session: AsyncSession
    create_user: CreateReturningGate[UserModel, CreateUserSchema, UserSchema]
    get_user: GetUserGate
    
    async def __call__(self, data: CreateUserSchema) -> UserSchema:
        async with self.session.begin():
            user = await self.get_user(UserLoginSchemas(phone=data.phone, email=data.email))
            if user is not None:
                raise UserAlreadyExistsError()
            return await self.create_user(data)
