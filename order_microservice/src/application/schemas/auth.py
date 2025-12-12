from uuid import UUID
from src.application.schemas.common import BaseModel

class AuthSchema(BaseModel):
    sub: UUID
    role: str
    token: str
