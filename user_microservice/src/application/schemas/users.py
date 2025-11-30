from uuid import UUID
from datetime import datetime, date
from src.application.schemas.common import BaseModel

class UserSchema(BaseModel):
    id: UUID
    first_name: str|None = None
    last_name: str|None = None
    middle_name: str|None = None
    birth_date: date|None = None
    phone: int
    email: str
    img:UUID|None = None
    created_at: datetime
    updated_at: datetime

class CreateUserSchema(BaseModel):
    id: UUID
    first_name: str|None = None
    last_name: str|None = None
    middle_name: str|None = None
    birth_date: date|None = None
    phone: int
    email: str
    img:UUID|None = None

class UpdateUserSchema(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    img:UUID|None = None
    updated_at: datetime


