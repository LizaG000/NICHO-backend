from uuid import UUID
from datetime import datetime
from src.application.schemas.common import BaseModel

class UserSchema(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    middle_name: str
    birth_date: datetime|None = None
    phone: int
    email: str
    img:UUID|None = None
    created_at: datetime
    updated_at: datetime

class CreateUserSchema(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    middle_name: str
    birth_date: datetime|None = None
    phone: int
    email: str
    img:UUID|None = None


