from uuid import UUID
from src.application.schemas.common import BaseModel

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




class ReturnProductSchema(BaseModel):
    productId: UUID
    price: float
    product: ProductSchema
    subProductPhotos: list[str]

class ReturnPaginationSchema(BaseModel):
    count: int
    items: list[ReturnProductSchema]

