from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import GetAllGate
from dataclasses import dataclass
from src.application.schemas.status import StatusSchema
from src.infra.postgres.tables import StatusModel
from src.application.schemas.auth import AuthSchema


@dataclass(slots=True, frozen=True, kw_only=True)
class GetStatusUsecase(Usecase[None, list[StatusSchema]]):
    session: AsyncSession
    auth: AuthSchema
    get_status: GetAllGate[StatusModel, StatusSchema]

    async def __call__(self, data: None) -> list[StatusSchema]:
        async with self.session.begin():
            return await self.get_status()
