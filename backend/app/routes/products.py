# /routes/products.py
from fastapi import APIRouter

router = APIRouter()

@router.post("/products")
def create_product():
    return {"message": "Product created"}

@router.get("/products")
def list_products():
    return {"message": "List of products"}

@router.get("/products/{id}")
def get_product(id: int):
    return {"message": f"Get product {id}"}

@router.put("/products/{id}")
def update_product(id: int):
    return {"message": f"Product {id} updated"}

@router.delete("/products/{id}")
def delete_product(id: int):
    return {"message": f"Product {id} deleted"}