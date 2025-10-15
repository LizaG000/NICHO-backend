import uuid
from datetime import datetime
from sqlalchemy import UUID
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import BigInteger
from sqlalchemy import DateTime
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
    __table_args__: dict[str, str] | tuple = {'schema': 'user_microservice_schema'}

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

class UserModel(BaseDBModel):
    __tablename__ = 'users'
    id: Mapped[uuid_pk]
    first_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    last_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    middle_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    birth_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    phone: Mapped[int] = mapped_column(
        BigInteger ,
        nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )
    img: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
        default=uuid.uuid4,
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

class AddressesModel(BaseDBModel):
    __tablename__ = 'addresses'
    id: Mapped[uuid_pk]
    id_user: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('user_microservice_schema.users.id'),
        nullable=False,
        default=uuid.uuid4,
    )
    country: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    region: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    city: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    street: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    house_number: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )
    quadrature_number: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )
    postal_code: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

class FavoritesModel(BaseDBModel):
    __tablename__ = 'favorites'
    id: Mapped[uuid_pk]
    id_user: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('user_microservice_schema.users.id'),
        nullable=False,
        default=uuid.uuid4,
    )
    id_product: Mapped[uuid.UUID] = mapped_column(
        UUID,
        nullable=False
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    
class BasketsModel(BaseDBModel):
    __tablename__ = 'baskets'
    id: Mapped[uuid_pk]
    id_user: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('user_microservice_schema.users.id'),
        nullable=False,
        default=uuid.uuid4,
    )
    id_product: Mapped[uuid.UUID] = mapped_column(
        UUID,
        nullable=False
    )
    count: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False
    )
    size: Mapped[str] = mapped_column(
        String,
        default="XS",
        nullable=False
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

class OrdersModel(BaseDBModel):
    __tablename__ = 'orders'
    id: Mapped[uuid_pk]
    id_user: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('user_microservice_schema.users.id'),
        nullable=False,
        default=uuid.uuid4,
    )
    id_addresses: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey('user_microservice_schema.addresses.id'),
        nullable=False
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

class OrdersProductsModel(BaseDBModel):
    __tablename__ = 'orders_products'
    id: Mapped[uuid_pk]
    id_order: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey('user_microservice_schema.orders.id'),
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


