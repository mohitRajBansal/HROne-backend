from fastapi import FastAPI
from app.routes import products, orders
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ Add CORS to allow frontend/API testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Register routes
app.include_router(products.router)
app.include_router(orders.router)
