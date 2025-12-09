from uuid import UUID
from datetime import datetime, date
from src.application.schemas.common import BaseModel

class StatusSchema(BaseModel):
    id: UUID
    name: str
    created_at: str


