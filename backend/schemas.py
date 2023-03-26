from pydantic import BaseModel


class Category(BaseModel):
    id: int
    title: str
    
    class Config:
        orm_mode = True


class Product(BaseModel):
    id: int
    title: str
    category_id: int
    
    class Config:
        orm_mode = True
