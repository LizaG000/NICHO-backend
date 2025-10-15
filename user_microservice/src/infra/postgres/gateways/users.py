from dataclasses import dataclass
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select
from src.infra.postgres.tables import UserModel
from src.usecase.users.schemas import UserLoginSchema
from src.application.schemas.users import UserSchema


@dataclass(slots=True, kw_only=True)
class PostgresGateway:
    session: AsyncSession

@dataclass(slots=True, kw_only=True)
class GetUserGate(PostgresGateway):

    async def __call__(self, login: UserLoginSchema) -> list[UserSchema]|None:
        stmt = Select(*UserModel.group_by_fields()).where(UserModel.email == login.email or UserModel.phone == login.phone)
        results = (await self.session.execute(stmt)).mappings().fetchall()
        logger.info(results)
        if results == []:
            return None
        return [UserSchema.model_validate(result) for result in results]
 