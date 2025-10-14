from uuid import UUID
from dataclasses import dataclass
from sqlalchemy import select, insert
from loguru import logger

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from tomlkit import table

from src.infra.postgres.tables import BaseDBModel
from sqlalchemy import Select
from sqlalchemy.sql.dml import ReturningInsert, ReturningUpdate
from typing import TypeVar, Generic, Type
from src.application.errors import DatabaseCreateError
from src.application.errors import NotFoundError

TAppliable = Select | ReturningInsert | ReturningUpdate

TTable = TypeVar('TTable', bound=BaseDBModel)
TEntity = TypeVar('TEntity', bound=BaseModel)
TCreate = TypeVar('TCreate', bound=BaseModel)
TEntityId = TypeVar('TEntityId', bound=UUID)

@dataclass(slots=True, kw_only=True)
class PostgresGateway:
    session: AsyncSession

@dataclass(slots=True, kw_only=True)
class GetAllByIdUserGate(Generic[TTable, TEntity, TEntityId], PostgresGateway):
    table: Type[TTable]
    schema_type: Type[TEntity]
    entity_id: Type[TEntityId]

    async def __call__(self, id_user = TEntityId) -> list[TEntity]:
        stmt = select(*self.table.group_by_fields()).where(self.table.id_user == id_user)
        results = (await self.session.execute(stmt)).mappings().fetchall()
        if results == []:
            raise  NotFoundError(self.table)
        return [self.schema_type.model_validate(result) for result in results]

@dataclass(slots=True, kw_only=True)
class CreateGate(Generic[TTable, TCreate], PostgresGateway):
    table: Type[TTable]
    create_schema_type: Type[TCreate]

    async def __call__(self, entity: TCreate) -> None:
        stmt = insert(self.table).values(**entity.model_dump())
        try:
            await self.session.execute(stmt)
        except:
            raise DatabaseCreateError(self.table)

@dataclass(slots=True, kw_only=True)
class CreateReturningGate(Generic[TTable, TCreate, TEntity], PostgresGateway):
    table: Type[TTable]
    create_schema_type: Type[TCreate]
    schema_type: Type[TEntity]

    async def __call__(self, entity: TCreate) -> TEntity:
        stmt = insert(self.table).values(**entity.model_dump()).returning(self.table)
        try:
            result = (await self.session.execute(stmt)).scalar_one().__dict__
            return self.schema_type.model_validate(result)
        except:
            raise DatabaseCreateError(self.table)


