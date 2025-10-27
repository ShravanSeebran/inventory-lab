from sqlalchemy.orm import Session
from app.schemas.inventory import ProductCreate
from app.db.repositories import inventory_repository

def create_product_service(db: Session, product: ProductCreate):
    return inventory_repository.create_product(db, product)

def get_product_service(db: Session, product_id: int):
    return inventory_repository.get_product(db, product_id)

def update_product_service(db: Session, product_id: int, updates: dict):
    return inventory_repository.update_product(db, product_id, updates)

def delete_product_service(db: Session, product_id: int):
    return inventory_repository.delete_product(db, product_id)
