from pydantic import BaseModel
from typing import List

class OrderItemIn(BaseModel):
    productId: str
    qty: int

class OrderIn(BaseModel):
    userId: str
    items: List[OrderItemIn]

class OrderOut(BaseModel):
    id: str
