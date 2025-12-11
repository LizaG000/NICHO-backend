from uuid import UUID
from pydantic import BaseModel, Field, field_validator

class GetCreateFavoritesSchema(BaseModel):
    id_product: UUID

class UserSchema(BaseModel):
    brandName: str

class ProductSchema(BaseModel):
    name: str
    description: str
    avgRating: float|None
    reviewsCount: int
    userId: UUID
    user: UserSchema
    categoryId: UUID
    category: str|None

class DesignerSchema(BaseModel):
    id: UUID
    brandName:str



class ReturnProductSchema(BaseModel):
    productId: UUID
    price: float
    product: ProductSchema
    photos: list[str] = Field(
        validation_alias="subProductPhotos",
        default_factory=list
    )
    user:DesignerSchema
    subProductSizes: list[dict] | str| None = None

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

class ReturnPaginationSchema(BaseModel):
    count: int
    items: list[ReturnProductSchema]

