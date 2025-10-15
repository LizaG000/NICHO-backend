import re
from uuid import UUID
from datetime import datetime, date
from pydantic import BaseModel, EmailStr, field_validator, Field
from src.application.schemas.common import BaseModel

class UserLoginSchemas(BaseModel):
    phone: int
    email: str

class CreateUserSchemas(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    middle_name: str
    birth_date: datetime | None = None
    phone: int
    email: EmailStr
    img: UUID | None = None

    @field_validator("first_name", "last_name", "middle_name")
    @classmethod
    def validate_and_format_names(cls, value: str) -> str:
        if not re.fullmatch(r"[A-Za-zА-Яа-яЁё\-]+", value):
            raise ValueError("Имя может содержать только буквы (латиница или кириллица) и дефис.")
        return value.capitalize()

    @field_validator("birth_date")
    @classmethod
    def validate_birth_date(cls, value: datetime | None) -> datetime | None:
        if value is None:
            return value
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < 14:
            raise ValueError("Пользователь должен быть не младше 14 лет.")
        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: int) -> int:
        if not re.fullmatch(r"8\d{10}", str(value)):
            raise ValueError("Телефон должен быть в формате 88005553535 (11 цифр, начинается с 8).")
        return value

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.strip().lower()
