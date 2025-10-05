from dataclasses import dataclass
from sqlalchemy import select, insert
from loguru import logger

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from src.infra.postgres.tables import BaseDBModel
from sqlalchemy import Select
from sqlalchemy.sql.dml import ReturningInsert, ReturningUpdate
from typing import TypeVar, Generic, Type


@dataclass(slots=True, kw_only=True)
class PostgresGateway:
    session: AsyncSession

@dataclass(slots=True, kw_only=True)
class GetUserGate(PostgresGateway):

    async def __call__(self) -> TEntity:
        stmt = select(*self.table.group_by_fields())
        logger.info(stmt)
        results = (await self.session.execute(stmt)).mappings().fetchall()
        logger.info(results)
        return [self.schema_type.model_validate(result) for result in results]
