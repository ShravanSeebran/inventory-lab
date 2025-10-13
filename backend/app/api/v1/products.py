# app/routes/products.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db import get_db
from app.schemas import ProductResponse, ProductUpdate

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int = Query(..., gt=0, description="Product ID must be positive"),
    db: Session = Depends(get_db)
):
    """
    Get a single product by ID
    
    - **product_id**: The ID of the product to retrieve
    - Returns: Product details if found
    """

    if product_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product ID must be positive"
        )

    if product_id > 1000:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    
  
    mock_product = {
        "id": product_id,
        "name": "Wireless Bluetooth Headphones",
        "description": "Noise cancelling wireless headphones with premium sound quality",
        "price": 249.99,
        "cost_price": 150.00,
        "quantity": 25,
        "category": "Audio",
        "sku": f"AUDIO-WH-{product_id}",
        "barcode": f"1234567890{product_id}",
        "weight": 0.3,
        "supplier_id": 1,
        "minimum_stock": 5,
        "is_active": True,
        "brand": "SoundMax",
        "dimensions": "18x15x8",
        "color": "Black",
        "size": "One Size",
        "is_tracked": True,
        "created_at": "2023-10-01T00:00:00",
        "updated_at": "2023-10-01T00:00:00"
    }
    
    return mock_product


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a product's information
    
    - **product_id**: The ID of the product to update
    - **product_data**: The fields to update (all fields optional)
    - Returns: Updated product details
    """

    if product_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product ID must be positive"
        )
    

    if product_id > 1000:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    

    update_data = product_data.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update"
        )
    

    mock_updated_product = {
        "id": product_id,
        "name": update_data.get("name", "Updated Wireless Headphones"),
        "description": update_data.get("description", "Updated noise cancelling headphones"),
        "price": update_data.get("price", 199.99),
        "cost_price": update_data.get("cost_price", 120.00),
        "quantity": update_data.get("quantity", 30),
        "category": update_data.get("category", "Audio"),
        "sku": update_data.get("sku", f"UPDATED-{product_id}"),
        "barcode": update_data.get("barcode", f"9876543210{product_id}"),
        "weight": update_data.get("weight", 0.35),
        "supplier_id": update_data.get("supplier_id", 1),
        "minimum_stock": update_data.get("minimum_stock", 3),
        "is_active": update_data.get("is_active", True),
        "brand": update_data.get("brand", "SoundMax Pro"),
        "dimensions": update_data.get("dimensions", "19x16x9"),
        "color": update_data.get("color", "Space Gray"),
        "size": update_data.get("size", "One Size"),
        "is_tracked": update_data.get("is_tracked", True),
        "created_at": "2023-10-01T00:00:00",
        "updated_at": "2023-10-15T14:30:00" 
    }
    
    return mock_updated_product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a product by ID
    
    - **product_id**: The ID of the product to delete
    - Returns: No content on success
    """

    if product_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product ID must be positive"
        )
    
    if product_id > 1000:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    
    print(f"Product {product_id} would be deleted here")
    
    return None 

@router.get("/", response_model=List[ProductResponse])
def get_all_products(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: Session = Depends(get_db)
):
    """
    Get all products with pagination
    
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Number of records to return (max 1000)
    - Returns: List of products
    """

    mock_products = [
        {
            "id": 1,
            "name": "Wireless Bluetooth Headphones",
            "description": "Noise cancelling wireless headphones",
            "price": 249.99,
            "cost_price": 150.00,
            "quantity": 25,
            "category": "Audio",
            "sku": "AUDIO-WH-001",
            "barcode": "1234567890123",
            "weight": 0.3,
            "supplier_id": 1,
            "minimum_stock": 5,
            "is_active": True,
            "brand": "SoundMax",
            "dimensions": "18x15x8",
            "color": "Black",
            "size": "One Size",
            "is_tracked": True,
            "created_at": "2023-10-01T00:00:00",
            "updated_at": "2023-10-01T00:00:00"
        },
        {
            "id": 2,
            "name": "Mechanical Gaming Keyboard",
            "description": "RGB mechanical gaming keyboard with blue switches",
            "price": 129.99,
            "cost_price": 80.00,
            "quantity": 15,
            "category": "Peripherals",
            "sku": "PERIPH-KB-002",
            "barcode": "1234567890124",
            "weight": 1.2,
            "supplier_id": 2,
            "minimum_stock": 3,
            "is_active": True,
            "brand": "KeyTech",
            "dimensions": "44x15x3",
            "color": "RGB",
            "size": "Full Size",
            "is_tracked": True,
            "created_at": "2023-10-02T00:00:00",
            "updated_at": "2023-10-02T00:00:00"
        }
    ]
    
    return mock_products[skip:skip + limit]