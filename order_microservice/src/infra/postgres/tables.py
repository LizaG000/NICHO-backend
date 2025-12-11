import uuid
from datetime import datetime
from sqlalchemy import UUID
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import BigInteger
from sqlalchemy import DateTime, Date
from sqlalchemy import func
from sqlalchemy import ForeignKey
from sqlalchemy import Float
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from typing import Annotated

uuid_pk = Annotated[uuid.UUID, mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid.uuid4,
    )]

created_at = Annotated[datetime, mapped_column(
    DateTime(timezone=True),
    default=func.now(), 
    nullable=False,

)]
updated_at = Annotated[datetime, mapped_column(
    DateTime(timezone=True),
    default=func.now(), 
    nullable=False,

)]

class BaseDBModel(DeclarativeBase):
    __tablename__: str
    __table_args__: dict[str, str] | tuple = {'schema': 'orders_microservice_schema'}

    @classmethod
    def group_by_fields(cls, exclude: list[str] | None = None) -> list:
        payload = []
        if not exclude:
            exclude = []

        for column in cls.__table__.columns:
            if column.key in exclude:
                continue

            payload.append(column)

        return payload


class OrdersModel(BaseDBModel):
    __tablename__ = 'orders'
    id: Mapped[uuid_pk]
    id_user: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        default=uuid.uuid4,
    )
    id_addresses: Mapped[uuid.UUID] = mapped_column(
        UUID,
        nullable=False
    )
    id_status: Mapped[uuid.UUID] = mapped_column(
        UUID,
        nullable=False
    )
    id_designer: Mapped[uuid.UUID] = mapped_column(
        UUID,
        nullable=False
    )
    price: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

class OrdersProductsModel(BaseDBModel):
    __tablename__ = 'orders_products'
    id: Mapped[uuid_pk]
    id_order: Mapped[uuid.UUID] = mapped_column(
        UUID,
        nullable=False
    )
    id_product: Mapped[uuid.UUID] = mapped_column(
        UUID,
        nullable=False
    )
    count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    size: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    price: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0
    )
    discount: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


class OrdersStatusModel(BaseDBModel):
    __tablename__ = 'order_status'
    id: Mapped[uuid_pk]
    id_order: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        default=uuid.uuid4,
    )
    id_status: Mapped[uuid.UUID] = mapped_column(
        UUID,
        nullable=False
    )
    created_at: Mapped[created_at]


class StatusModel(BaseDBModel):
    __tablename__ = 'status'
    id: Mapped[uuid_pk]
    status: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    created_at: Mapped[created_at]
