from uuid import UUID
from datetime import datetime
from src.application.schemas.common import BaseModel

class AddressSchemas(BaseModel):
    id: UUID
    id_user: UUID
    country: str
    region: str
    city: str
    street: str
    house_number: str
    quadrature_number: str
    postal_code: str
    created_at: datetime
    updated_at: datetime

class CreateAddressSchemas(BaseModel):
    id_user: UUID
    country: str
    region: str
    city: str
    street: str
    house_number: str
    quadrature_number: str
    postal_code: str
    