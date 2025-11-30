from uuid import UUID
from datetime import datetime
from src.application.schemas.common import BaseModel
from pydantic import field_validator, Field

class AddressSchema(BaseModel):
    id: UUID
    id_user: UUID
    country: str = Field(..., min_length=1)
    region: str = Field(..., min_length=1)
    city: str = Field(..., min_length=1)
    street: str = Field(..., min_length=1)
    house_number: str = Field(..., min_length=1)
    quadrature_number: str = Field(..., min_length=1)
    postal_code: int
    created_at: datetime
    updated_at: datetime

    @field_validator('country', 'region', 'city', 'street', 'house_number', 'quadrature_number')
    @classmethod
    def validate_non_empty_strings(cls, v: str, info) -> str:
        if isinstance(v, str) and v.strip() == '':
            raise ValueError(f'{info.field_name} cannot be empty or whitespace only')
        return v.strip()

class CreateAddressSchema(BaseModel):
    id_user: UUID
    country: str
    region: str
    city: str
    street: str
    house_number: str
    quadrature_number: str
    postal_code: int


