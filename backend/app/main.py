from fastapi import FastAPI
from routes import products, suppliers, transactions, users # Import all routers
from .database import engine, Base

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Inventory Lab API running"}

# Include all the new routers
app.include_router(products.router)
app.include_router(suppliers.router)
app.include_router(transactions.router)
app.include_router(users.router)
