# HROne Backend Task - FastAPI + MongoDB

## Endpoints

### POST /products
Create a product

### GET /products
List products with filters (name, size) + pagination

### POST /orders
Create an order with productId and qty

### GET /orders/{userId}
List orders of user with product lookup

## Run
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Setup
- Create `.env` file with your Mongo URI
- Use MongoDB Atlas (M0 Free)

## Deployment
Ready for Render.com or Railway.app
