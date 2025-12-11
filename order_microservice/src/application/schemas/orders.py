from uuid import UUID
from datetime import datetime, timezone
from src.application.schemas.common import BaseModel

class OrderSchema(BaseModel):
    id: UUID
    id_user: UUID
    id_address: UUID
    id_status: UUID
    id_designer: UUID
    status: str
    price: float
    created_at: datetime
    updated_at: datetime

class CreateOrderSchema(BaseModel):
    id_user: UUID
    id_address: UUID
    id_status: UUID
    id_designer: UUID
    price: float


class UpdateOrderSchema(BaseModel):
    id_status: UUID
    updated_at: datetime = datetime.now(timezone.utc)
