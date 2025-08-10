from fastapi import FastAPI
from routes import products

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Inventory Lab API running"}

app.include_router(products.router)