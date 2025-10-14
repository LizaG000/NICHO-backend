from uuid import UUID
from datetime import datetime
from src.application.schemas.common import BaseModel

class AddressSchema(BaseModel):
    id: UUID
    id_user: UUID
    country: str
    region: str
    city: str
    street: str
    house_number: str
    quadrature_number: str
    postal_code: int
    created_at: datetime
    updated_at: datetime

class CreateAddressSchema(BaseModel):
    id_user: UUID
    country: str
    region: str
    city: str
    street: str
    house_number: str
    quadrature_number: str
    postal_code: int


