from fastapi import APIRouter, Query
from app.database import product_collection
from app.models.product import ProductIn, ProductOut
from bson import ObjectId

router = APIRouter()

@router.post("/products", response_model=ProductOut, status_code=201)
def create_product(product: ProductIn):
    result = product_collection.insert_one(product.dict())
    return {"id": str(result.inserted_id)}

@router.get("/products")
def list_products(
    name: str = Query(None),
    size: str = Query(None),
    limit: int = Query(10),
    offset: int = Query(0),
):
    query = {}
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if size:
        query["sizes.size"] = size

    cursor = product_collection.find(query).skip(offset).limit(limit)
    products = []
    for p in cursor:
        products.append({
            "id": str(p["_id"]),
            "name": p["name"],
            "price": p["price"]
        })

    return {
        "data": products,
        "page": {
            "next": offset + limit,
            "limit": len(products),
            "previous": max(offset - limit, 0)
        }
    }
