from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from datetime import datetime

from ..database import Base

class Product(Base):
    """Core inventory product table"""
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(String(500))
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    category = Column(String(50), index=True)
    sku = Column(String(50), unique=True, index=True)
    barcode = Column(String(100), unique=True)
    weight = Column(Float)  # in grams
    supplier_id = Column(Integer, ForeignKey('suppliers.id'), index=True)
    minimum_stock = Column(Integer, default=5)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Supplier(Base):
    """Supplier information table"""
    __tablename__ = 'suppliers'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    contact_person = Column(String(100))
    email = Column(String(100))
    phone = Column(String(20))
    address = Column(String(200))
    tax_id = Column(String(50))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class InventoryTransaction(Base):
    """Tracks all inventory movements"""
    __tablename__ = 'inventory_transactions'
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False, index=True)
    transaction_type = Column(String(20), nullable=False)  # 'purchase', 'sale', 'adjustment', 'return'
    quantity = Column(Integer, nullable=False)
    reference_id = Column(String(100))  # PO number, sale ID, etc.
    notes = Column(String(200))
    created_by = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

class User(Base):
    """System users table (for future auth)"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(200), nullable=False)
    full_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)