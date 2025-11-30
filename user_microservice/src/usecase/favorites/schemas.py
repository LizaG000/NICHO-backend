from uuid import UUID
from src.application.schemas.common import BaseModel

class GetCreateFavoritesSchema(BaseModel):
    id_product: UUID