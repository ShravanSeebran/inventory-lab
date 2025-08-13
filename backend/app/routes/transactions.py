from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, models
from ..database import get_db

router = APIRouter(
    prefix="/transactions",
    tags=["inventory transactions"]
)

# Endpoint to create a new inventory transaction
@router.post("/", response_model=schemas.InventoryTransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(transaction: schemas.InventoryTransactionCreate, db: Session = Depends(get_db)):
    db_transaction = models.InventoryTransaction(**transaction.model_dump())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

# Endpoint to get a list of all transactions
@router.get("/", response_model=List[schemas.InventoryTransactionResponse])
def get_all_transactions(db: Session = Depends(get_db)):
    transactions = db.query(models.InventoryTransaction).all()
    return transactions

# Endpoint to get a single transaction by ID
@router.get("/{transaction_id}", response_model=schemas.InventoryTransactionResponse)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    db_transaction = db.query(models.InventoryTransaction).filter(models.InventoryTransaction.id == transaction_id).first()
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction

# Endpoint to delete a transaction (useful for correcting errors)
@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    db_transaction = db.query(models.InventoryTransaction).filter(models.InventoryTransaction.id == transaction_id).first()
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    db.delete(db_transaction)
    db.commit()
    return {"message": "Transaction deleted successfully"}