from uuid import UUID
from datetime import datetime
from src.application.schemas.common import BaseModel

class FavoriteSchema(BaseModel):
    id: UUID
    id_user: UUID
    id_product: UUID
    size: str
    created_at: datetime
    updated_at: datetime

class CreateFavoriteSchema(BaseModel):
    size: str
    id_user: UUID
    id_product: UUID