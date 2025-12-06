from uuid import UUID
from datetime import datetime, timezone
from src.application.schemas.common import BaseModel

class BasketSchema(BaseModel):
    id: UUID
    id_user: UUID
    id_product: UUID
    count: int
    size: str | None = None
    created_at: datetime
    updated_at: datetime

class CreateBasketSchema(BaseModel):
    id_user: UUID
    id_product: UUID
    count: int
    size: str | None = None
    created_at: datetime

class UpdateBasketSchema(BaseModel):
    count: int | None = None
    size: str | None = None
    updated_at: datetime = datetime.now(timezone.utc)

