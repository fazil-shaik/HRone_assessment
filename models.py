"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from bson import ObjectId

class SizeInfo(BaseModel):
    size: str
    quantity: int

class ProductCreate(BaseModel):
    name: str
    price: float
    sizes: List[SizeInfo]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "iPhone 14 Pro",
                "price": 999.99,
                "sizes": [
                    {
                        "size": "large",
                        "quantity": 50
                    }
                ]
            }
        }

class Product(BaseModel):
    id: str = Field(alias="_id")
    name: str
    price: float
    sizes: List[SizeInfo]
    created_at: datetime

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

class OrderItem(BaseModel):
    productid: str
    qty: int

    class Config:
        json_schema_extra = {
            "example": {
                "productid": "507f1f77bcf86cd799439011",
                "qty": 3
            }
        }

class OrderCreate(BaseModel):
    items: List[OrderItem]
    total_amount: float
    user_address: Dict[str, Any]

    class Config:
        json_schema_extra = {
            "example": {
                "items": [
                    {
                        "productid": "507f1f77bcf86cd799439011", 
                        "qty": 3
                    }
                ],
                "total_amount": 1999.98,
                "user_address": {
                    "user_id": "user123",
                    "street": "123 Main Street",
                    "city": "New York",
                    "state": "NY",
                    "zip": "10001",
                    "country": "USA"
                }
            }
        }

class Order(BaseModel):
    id: str = Field(alias="_id")
    items: List[OrderItem]
    total_amount: float
    user_address: Dict[str, Any]
    created_at: datetime

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

class ProductsResponse(BaseModel):
    data: List[Product]
    page: Dict[str, Any]

class OrdersResponse(BaseModel):
    data: List[Order]
    page: Dict[str, Any]

class HealthResponse(BaseModel):
    status: str
    database: str
    message: Optional[str] = None
    error: Optional[str] = None
