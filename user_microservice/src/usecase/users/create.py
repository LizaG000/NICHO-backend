from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import CreateGate
from src.application.schemas.users import CreateUserSchema
from src.infra.postgres.tables import UserModel
from dataclasses import dataclass
from src.infra.postgres.gateways.users import GetUserGate
from src.usecase.users.schemas import UserLoginSchemas
from src.application.errors import UserAlreadyExistsError

@dataclass(slots=True, frozen=True, kw_only=True)
class CreateUserUsecase(Usecase[CreateUserSchema, None]):
    session: AsyncSession
    create_user: CreateGate[UserModel, CreateUserSchema]
    get_user: GetUserGate
    
    async def __call__(self, data: CreateUserSchema) -> None:
        async with self.session.begin():
            user = await self.get_user(UserLoginSchemas(phone=data.phone, email=data.email))
            if user is not None:
                raise UserAlreadyExistsError()
            await self.create_user(data)
