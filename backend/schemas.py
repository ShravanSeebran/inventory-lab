from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional

# --- Product Schemas ---
class ProductBase(BaseModel):
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    quantity: int = Field(..., ge=0)
    category: Optional[str] = None
    sku: Optional[str] = None
    barcode: Optional[str] = None
    weight: Optional[float] = None
    supplier_id: Optional[int] = None
    minimum_stock: int = Field(5, ge=0)
    is_active: bool = True

class ProductCreate(ProductBase):
    # This is for creating a new product. It is the same as ProductBase for now.
    pass

class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- Supplier Schemas ---
class SupplierBase(BaseModel):
    name: str = Field(..., min_length=1)
    contact_person: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    tax_id: Optional[str] = None
    is_active: bool = True

class SupplierCreate(SupplierBase):
    pass

class SupplierResponse(SupplierBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- Inventory Transaction Schemas ---
class InventoryTransactionBase(BaseModel):
    product_id: int
    transaction_type: str = Field(..., pattern="^(purchase|sale|adjustment|return)$")
    quantity: int
    reference_id: Optional[str] = None
    notes: Optional[str] = None
    created_by: Optional[str] = None

class InventoryTransactionCreate(InventoryTransactionBase):
    pass

class InventoryTransactionResponse(InventoryTransactionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- User Schemas ---
class UserBase(BaseModel):
    username: str = Field(..., min_length=3)
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    is_admin: bool = False

class UserCreate(UserBase):
    hashed_password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    last_login: Optional[datetime]

    class Config:
        from_attributes = True