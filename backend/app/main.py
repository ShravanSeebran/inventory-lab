from fastapi import FastAPI
from app.api.v1.users import router as user_router
from app.api.v1 import products
app.include_router(products.router, prefix="/api/v1")
app = FastAPI()

app.include_router(user_router)


@app.get("/")
def home():
    return {"message": "hello world!"}

