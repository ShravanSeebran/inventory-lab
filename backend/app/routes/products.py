from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

#This basically imports from the parent directory
from .. import schemas, models
# this imports from the database session dependency
from ..database import get_db

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

# The endpoint to create a new product
@router.post("/", response_model=schemas.ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# The endpoint to get a list of all the products
@router.get("/", response_model=List[schemas.ProductResponse])
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products

# The endpoint to get a single product by ID
@router.get("/{product_id}", response_model=schemas.ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

#The endpoint to update a product
@router.put("/{product_id}", response_model=schemas.ProductResponse)
def update_product(product_id: int, updated_product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in updated_product.model_dump().items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product

#The endpoint to delete a product
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}
