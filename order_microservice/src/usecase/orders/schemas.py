from uuid import UUID
from src.application.schemas.order_products import OrderProductSchema
from datetime import datetime, timezone
from pydantic import BaseModel, Field, field_validator

class ReturnProduct(OrderProductSchema):
    color: list[dict] | str| None = None
    photos: list[str]



class CreateProductModel(BaseModel):
    id_product: UUID
    count: int
    size: str
    price: float
    discount: float


class GetCreateOrderSchema(BaseModel):
    id_user: UUID
    id_address: UUID
    id_designer: UUID
    status: str
    products: list[CreateProductModel]

class ReturnOrderSchema(BaseModel):
    id: UUID
    id_user: UUID
    id_address: UUID
    id_designer: UUID
    price: float
    status: str
    created_at: datetime
    updated_at: datetime
    products: list[OrderProductSchema]

class ReturnAllOrders(BaseModel):
    id: UUID
    id_user: UUID
    id_designer: UUID
    address: dict | UUID
    price: float
    status: str
    created_at: datetime

class ReturnOrdersPagination(BaseModel):
    orders: list[ReturnAllOrders]
    limit_left: int | None
    offset_left: int | None
    limit_right: int | None
    offset_right: int | None
    items: int

class ProductSchema(BaseModel):
    name: str
    description: str
    avgRating: float|None
    reviewsCount: int
    userId: UUID
    categoryId: UUID
    category: str|None

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

class ReturnProductSchema(BaseModel):
    productId: UUID
    price: float
    product: ProductSchema
    photos: list[str] = Field(
        validation_alias="subProductPhotos",
        default_factory=list
    )
    subProductSizes: list[dict] | str| None = None
    color: list[dict] | str| None = None

    @field_validator('photos', mode='before')
    @classmethod
    def extract_photo_refs(cls, v):
        """Преобразуем список словарей в список строк photoRef"""
        if not v or v == []:
            return []

        if isinstance(v, list) and v and isinstance(v[0], dict):
            # Извлекаем только photoRef из каждого словаря
            result = []
            for item in v:
                if isinstance(item, dict) and 'photoRef' in item:
                    result.append(item['photoRef'])
            return result

        return v

    class Config:
        populate_by_name = True

class GetUpdateOrderSchema(BaseModel):
    id: UUID
    id_status: UUID
    updated_at: datetime = datetime.now(timezone.utc)


class ReturnAllOrdersSchemas(BaseModel):
    id: UUID
    id_user: UUID
    id_designer: UUID
    address: AddressSchema | UUID
    price: float
    status: str
    created_at: datetime
    products: list[ReturnProduct]
