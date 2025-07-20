from fastapi import APIRouter, Path, Query
from bson import ObjectId
from app.database import order_collection, product_collection
from app.models.order import OrderIn, OrderOut

router = APIRouter()

# -------------------- POST /orders --------------------
@router.post("/orders", response_model=OrderOut, status_code=201)
def create_order(order: OrderIn):
    order_data = {
        "userId": order.userId,
        "items": order.items
    }
    result = order_collection.insert_one(order_data)
    return {"id": str(result.inserted_id)}

# -------------------- GET /orders/{user_id} --------------------
@router.get("/orders/{user_id}")
def list_orders(
    user_id: str = Path(..., description="User ID"),
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0),
):
    query = {"userId": user_id}
    cursor = order_collection.find(query).skip(offset).limit(limit)

    orders = []

    for order in cursor:
        item_list = []
        total = 0

        for item in order.get("items", []):
            product = product_collection.find_one({"_id": ObjectId(item["productId"])})
            if product:
                product_detail = {
                    "id": str(product["_id"]),
                    "name": product["name"]
                }
                qty = item["qty"]
                total += qty * product["price"]
                item_list.append({
                    "productDetails": product_detail,
                    "qty": qty
                })

        orders.append({
            "id": str(order["_id"]),
            "items": item_list,
            "total": total
        })

    return {
        "data": orders,
        "page": {
            "next": offset + limit,
            "limit": len(orders),
            "previous": max(offset - limit, 0)
        }
    }
