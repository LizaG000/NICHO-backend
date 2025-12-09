from uuid import UUID
from datetime import datetime, date
from src.application.schemas.common import BaseModel

class OrderSchema(BaseModel):
    id: UUID
    id_user: UUID
    id_address: UUID
    id_status: UUID
    status: str
    price: float
    created_at: datetime
    updated_at: datetime

class CreateOrderSchema(BaseModel):
    id_user: UUID
    id_address: UUID
    id_status: UUID
    price: float

