from dataclasses import dataclass
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select
from src.infra.postgres.tables import StatusModel
from src.application.schemas.status import StatusSchema


@dataclass(slots=True, kw_only=True)
class PostgresGateway:
    session: AsyncSession


@dataclass(slots=True, kw_only=True)
class GetStatusGate(PostgresGateway):

    async def __call__(self, name: str) -> StatusSchema | None:
        stmt = Select(*StatusModel.group_by_fields()).where(
            StatusModel.name == name)
        result = (await self.session.execute(stmt)).mappings().fetchone()
        logger.info(result)
        if result is None:
            return None
        return StatusSchema.model_validate(result)

