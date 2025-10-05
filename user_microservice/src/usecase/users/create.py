from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import CreateGate
from src.application.schemas.users import CreateUserSchema
from src.infra.postgres.tables import UserModel
from dataclasses import dataclass

@dataclass(slots=True, frozen=True, kw_only=True)
class CreateUserUsecase(Usecase[CreateUserSchema, None]):
    session: AsyncSession
    create_user: CreateGate[UserModel, CreateUserSchema]
    
    async def __call__(self, data: CreateUserSchema) -> None:
        async with self.session.begin():
            # проверка на валидность входящих е-маил, телефон, имени и возраста
            # поиск пользователей с таким е-маил и почтой
            # создание записи
            await self.create_user(data)
