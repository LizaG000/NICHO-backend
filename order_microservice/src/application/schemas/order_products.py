from uuid import UUID
from datetime import datetime, date
from src.application.schemas.common import BaseModel

class OrderProductSchema(BaseModel):
    id: UUID
    id_order: UUID
    id_product: UUID
    count: int
    size: str
    price: float
    discount: float
    created_at: datetime
    updated_at: datetime

class CreateOrderProductSchema(BaseModel):
    id_order: UUID
    id_product: UUID
    count: int
    size: str
    price: float
    discount: float

