from dataclasses import dataclass
from sqlalchemy import select, insert
from loguru import logger

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from src.infra.postgres.tables import BaseDBModel
from sqlalchemy import Select
from sqlalchemy.sql.dml import ReturningInsert, ReturningUpdate
from typing import TypeVar, Generic, Type
from src.infra.postgres.tables import AddressesModel
from src.application.schemas.addresses import CreateAddressSchema, AddressSchema
from loguru import logger

@dataclass(slots=True, kw_only=True)
class PostgresGateway:
    session: AsyncSession


@dataclass(slots=True, kw_only=True)
class GetAddressGate(PostgresGateway):

    async def __call__(self, address: CreateAddressSchema) -> AddressSchema | None:
        logger.info((address))
        stmt = Select(*AddressesModel.group_by_fields()).where(
            (AddressesModel.id_user == address.id_user) &
            (AddressesModel.country == address.country) &
            (AddressesModel.region == address.region) &
            (AddressesModel.city == address.city) &
            (AddressesModel.street == address.street) &
            (AddressesModel.house_number == address.house_number) &
            (AddressesModel.quadrature_number == address.quadrature_number) &
            (AddressesModel.postal_code == address.postal_code)
        )
        results = (await self.session.execute(stmt)).mappings().fetchone()
        logger.info(results)
        if results is None:
            return None
        return AddressSchema.model_validate(results)
